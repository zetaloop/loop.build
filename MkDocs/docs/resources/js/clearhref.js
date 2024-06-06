document$.subscribe(function () {
    var links = document.querySelectorAll("a");
    links.forEach(function (link) {
        if (!link.getAttribute("href")) {
            link.setAttribute("href", "javascript:''.什么都不会发生");
        }
    });
});
