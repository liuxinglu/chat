$(document).ready(function () {
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

        // 使用AJAX加载index.html的内容
        $.ajax({
            url: '/pageops/getBankPage', // 确保这里的路径是正确的
            method: 'GET',
            success: function(data) {
                // 将加载的内容放入#content-container中
                $('#container-fluid').html(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error loading index.html: ' + textStatus, errorThrown);
            }
        });
    });

    $('#userKeyword').click(function(e) {
        e.preventDefault(); // 阻止默认的链接跳转行为

        // 使用AJAX加载index.html的内容
        $.ajax({
            url: '/pageops/getKeywordPage', // 确保这里的路径是正确的
            method: 'GET',
            success: function(data) {
                // 将加载的内容放入#content-container中
                $('#container-fluid').html(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error loading index.html: ' + textStatus, errorThrown);
            }
        });
    });

    $('#userChat').click(function(e) {
        e.preventDefault(); // 阻止默认的链接跳转行为

        // 使用AJAX加载index.html的内容
        $.ajax({
            url: '/pageops/getChatPage', // 确保这里的路径是正确的
            method: 'GET',
            success: function(data) {
                // 将加载的内容放入#content-container中
                $('#container-fluid').html(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error loading index.html: ' + textStatus, errorThrown);
            }
        });
    });

    $('#usersCollapse2').click(function(e) {
        e.preventDefault(); // 阻止默认的链接跳转行为

        // 使用AJAX加载index.html的内容
        $.ajax({
            url: '/pageops/getBankPage', // 确保这里的路径是正确的
            method: 'GET',
            success: function(data) {
                // 将加载的内容放入#content-container中
                $('#container-fluid').html(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error loading index.html: ' + textStatus, errorThrown);
            }
        });
    });
});