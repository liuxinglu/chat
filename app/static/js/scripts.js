$(document).ready(function () {

    var pictures = ["homepic01.jpg", "homepic02.jpg", "homepic03.jpg", "homepic04.jpg"]; // 图片名称数组
    var currentIndex = 0; // 当前显示的图片索引
    var intervalId; // 定时器ID
    var cachedImages = {}; // 用于存储已获取的图片Blob数据
    var imagesLoaded = 0; // 记录已加载的图片数量

    // 加载并显示图片的函数（现在会检查是否已缓存）
    function loadAndShowPic(picName) {
        if (cachedImages[picName]) {
            // 如果图片已缓存，则直接使用缓存中的图片
            showPic(cachedImages[picName]);
        } else {
            // 如果图片未缓存，则从后端获取
            $.ajax({
                url: '/ad/getPic/' + encodeURIComponent(picName),
                type: 'POST',
                xhrFields: {
                    responseType: 'blob'
                },
                success: function(blob, textStatus, jqXHR) {
                    // 存储图片Blob数据到缓存中
                    cachedImages[picName] = blob;
                    // 显示图片
                    showPic(blob);

                    // 增加已加载的图片数量（用于检查是否所有图片都已加载完毕）
                    imagesLoaded++;
                    if (imagesLoaded === pictures.length) {
                        // 如果所有图片都已加载，则开始轮播
                        startCarousel();
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error('There has been a problem with your AJAX operation:', textStatus, errorThrown);
                }
            });
        }
    }

    // 显示图片的函数（从缓存中加载）
    function showPic(blob) {
        const url = URL.createObjectURL(blob);
        const img = $('<img>').attr('src', url).addClass('col-md-12');
        $('#ad_pic').empty(); // 清空之前的图片
        $('#ad_pic').append(img);

        setTimeout(function() {
            URL.revokeObjectURL(url); // 释放URL对象
        }, 10000); // 10秒后释放（可以根据需要调整）
    }

    // 开始轮播的函数（现在会在所有图片加载完毕后自动调用）
    function startCarousel() {
        // 由于所有图片都已加载到缓存中，因此可以直接开始轮播
        setInterval(function () {
            currentIndex = (currentIndex + 1) % pictures.length;
            showPic(cachedImages[pictures[currentIndex]]);
        }, 3000); // 每3秒切换一次图片
    }

    // 初始化：加载所有图片（注意：这里不再直接调用startCarousel，而是等待所有图片加载完毕）
    pictures.forEach(function(picName) {
        loadAndShowPic(picName); // 首次调用时会加载图片，但不会立即开始轮播
    });

    if ($('#flash-messages1 li').length > 0) {
        // 等待动画完成后再设置定时器隐藏flash消息
        setTimeout(function() {
            $('#flash-messages1 li').each(function(index) {
                // 为每个flash消息元素添加淡出动画
                $(this).fadeOut(500, function() {
                    // 淡出完成后添加hidden类以隐藏元素（可选，因为fadeOut已经隐藏了元素）
                    $(this).addClass('hidden');
                });
                // 如果你想要它们逐个消失，可以使用延迟
                setTimeout(function() { $(this).fadeOut(500); }.bind(this), index * 500);
            });
            // 如果你想要整个列表在动画完成后从DOM中移除（可选）
            //$('#flash-messages1').remove();
        }, 1000 + 500); // 1000ms等待动画完成，再加上500ms的fadeOut时间
    }


    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
        // 切换按钮文本
        var $this = $(this);
        if ($this.find('.icon').text() === '◀') {
            $this.attr('aria-expanded', 'true');
            $this.find('.icon').text('▶');
        } else {
            $this.attr('aria-expanded', 'false');
            $this.find('.icon').text('◀');
        }
    });

    $('.navbar-toggler').click(function() {
        var isExpanded = $('#navbarNav').hasClass('show');
        $('#menu-toggle').text(isExpanded ? '<<' : '>>');
    });

    document.querySelectorAll('#sidebar-wrapper .list-group-item').forEach(function(item) {
        item.addEventListener('click', function() {
            // 移除所有列表项上的.active类
            document.querySelectorAll('#sidebar-wrapper .list-group-item.active').forEach(function(activeItem) {
                activeItem.classList.remove('active');
            });

            // 为当前点击的列表项添加.active类
            this.classList.add('active');
        });
    });

    $('#modelSelector').change(function() {
        var selectedModel = $(this).val();

        // 使用jQuery的$.ajax方法发送POST请求到后端
        $.ajax({
            url: '/pageops/selectModel',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ model: selectedModel }),
            success: function(data) {
                var myToast = new bootstrap.Toast(document.getElementById('toast-container'));
                var message = data.model || '操作成功';
                  var toastBody = $('#toast-container .toast-body').text("已选模型"+message);

                  // 显示 Toast
                  myToast.show();

                  // 如果需要，可以在一段时间后自动关闭 Toast
                  setTimeout(function() {
                    myToast.hide();
                  }, 1500); // 1.5秒后关闭
            }
        });
    });

    // 监听侧边栏链接的点击事件
    $('#dashboard').click(function(e) {
        e.preventDefault(); // 阻止默认的链接跳转行为
        var $menusContainer = $('#menus');
        $menusContainer.empty();
        var arr = [
            {"id":"domain", "content":'AI Domain Solution'},
            {"id":"servicedesk", "content":'AI Service Desk'},
            {"id":"security", "content":'AI Security Solution'},
            {"id":"cloud", "content":'AI Cloud Solution'}];
        arr.forEach(
            function(menuItem) {
                var $a = $('<a>', {
                    href: '#',
                    'class': 'list-group-item list-group-item-action btn btn-link',
                    text: menuItem.content
                }).attr('id', menuItem.id);
                $menusContainer.append($a);
            });
        $('#container-fluid').empty();
        var htmldata = `<div id="default" class="row justify-content-center mt-4">
                            <div class="col-md-12">
                                <div id="ad_pic" class="col-md-12">
                                </div>
                            </div>
                        </div>`;
        $('#container-fluid').html(htmldata)
        startCarousel();
    });



    // 使用事件委托绑定动态元素的事件
    $('#menus').on('click', '#domain, #servicedesk', function(e) {
        e.preventDefault();
        var $this = $(this);
        var url = '/pageops/servicedesk';
        if ($this.is('#domain')){
            url = '/pageops/domain';
        }
        else if($this.is('#servicedesk')) {
            url ='/pageops/servicedesk';
        }
        loadMenuAndContent($this.attr('id'), url);
    });

    function loadMenuAndContent(elementId, menuUrl) {
        $.ajax({
            url: menuUrl,
            method: 'GET',
            success: function(data) {
                var $menusContainer = $('#menus');
                $menusContainer.empty();
                data.menu.forEach(function(menuItem) {
                    var $a = $('<a>', {
                        href: '#',
                        'class': 'list-group-item list-group-item-action btn btn-link',
                        text: menuItem.content
                    }).attr('id', menuItem.id);
                    $menusContainer.append($a);
                });

                // 假设 #userKeyword 或 #userChat 是新加载的菜单项之一，它们的事件已经被上面的事件委托处理了
                // 因此，这里不需要再次绑定它们的事件
                $('#userKeyword, #userChat, #servicedeskops_TicketCreation, #securityops, #cloudops').on('click', function(e) {
                    e.preventDefault();
                    var url = ' ';
                    if($(this).is('#userKeyword')) {
                        url = '/pageops/userKeyword';
                    }
                    else if ($(this).is('#servicedeskops_TicketCreation')){
                        url = '/pageops/servicedeskops_TicketCreation';
                    }
                    loadContent(url);
                });
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error loading menu: ' + textStatus, errorThrown);
                // 可以在这里向用户显示错误消息
            }
        });
    }

    function loadContent(contentUrl) {
        $.ajax({
            url: contentUrl,
            method: 'GET',
            success: function(data) {
                $('#container-fluid').html(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error loading content: ' + textStatus, errorThrown);
                // 可以在这里向用户显示错误消息
            }
        });
    }



});