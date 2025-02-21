var pictures = ["homepic01.jpg", "homepic02.jpg", "homepic03.jpg", "homepic04.jpg"]; // 图片名称数组
let cachedImages = {};
let imagesLoaded = 0;
let carouselInterval; // 定时器变量

$(document).ready(function () {
    initPic();
});

// 走马灯逻辑
export function startCarousel() {
    let currentIndex = 0;
    const images = document.querySelectorAll('.carousel-image');
    const totalImages = images.length;
    let navdots = document.querySelectorAll('.nav-dot');

    function showNextImage() {
        images.forEach((img, i) => {
            img.classList.toggle('active', i === currentIndex);
        });
        navdots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentIndex);
        });
        currentIndex = (currentIndex + 1) % totalImages;
    }

    carouselInterval = setInterval(showNextImage, 3000); // 每3秒切换一次图片

    // 为底部导航点添加点击事件（假设导航点已经存在于DOM中）
    document.querySelectorAll('.nav-dot').forEach((dot, i) => {
        dot.addEventListener('click', () => {
            clearInterval(carouselInterval); // 停止定时器
            currentIndex = i; // 更新当前索引
            showNextImage(); // 显示当前索引的图片（实际上是显示下一张，但因为索引已更新，所以看起来是正确的）
            carouselInterval = setInterval(showNextImage, 3000); // 重新启动定时器
        });
    });
}

// 初始化图片加载
export function initPic() {
// 显示图片的函数
    function showPic(blob, index) {
        const imgElement = document.querySelector(`.carousel-image[data-index="${index}"]`);
        const url = URL.createObjectURL(blob);
        imgElement.src = url;
//        如果你担心内存泄漏，可以在图片不再需要时（比如切换到下一张图片时）释放之前的URL
//        URL.revokeObjectURL(url); // 释放URL对象
    }

    // 加载并显示图片的函数
    function loadAndShowPic(picName, index) {
        if (cachedImages[picName]) {
            showPic(cachedImages[picName], index);
        } else {
            $.ajax({
                url: '/ad/getPic/' + encodeURIComponent(picName),
                type: 'POST',
                xhrFields: {
                    responseType: 'blob'
                },
                success: function(blob, textStatus, jqXHR) {
                    cachedImages[picName] = blob;
                    showPic(blob, index);
                    imagesLoaded++;
                    if (imagesLoaded === pictures.length) {
                        startCarousel();
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error('Error loading image:', textStatus, errorThrown);
                }
            });
        }
    }
    pictures.forEach((picName, index) => {
        const imgElement = document.createElement('img');
        imgElement.classList.add('carousel-image');
        imgElement.dataset.index = index; // 为每个图片元素添加一个data-index属性来标识其索引
        document.querySelector('.carousel').appendChild(imgElement); // 假设.carousel是你的图片容器
        loadAndShowPic(picName, index); // 加载并显示图片
    });
}