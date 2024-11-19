$(document).ready(function () {
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
                console.log('Success:', data);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    // 监听侧边栏链接的点击事件
    $('#usersCollapse').click(function(e) {
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