document$.subscribe(function () {
    var links = document.querySelectorAll("a");
    links.forEach(function (link) {
        if (!link.getAttribute("href")) {
            link.setAttribute("href", "javascript:''.一个空白的链接");
            link.style.cursor = "auto";
        }
    });
});
