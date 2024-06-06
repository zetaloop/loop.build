document$.subscribe(function () {
    var links = document.querySelectorAll("a");
    links.forEach(function (link) {
        if (!link.getAttribute("href")) {
            link.setAttribute(
                "href",
                "javascript:'>>>'.点击这个链接什么都不会发生"
            );
        }
    });
});
