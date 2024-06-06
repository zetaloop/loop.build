document$.subscribe(function () {
    var links = document.querySelectorAll("a");
    links.forEach(function (link) {
        if (!link.getAttribute("href")) {
            link.removeAttribute("href");
            link.style.cursor = "auto";
            link.addEventListener("click", function (e) {
                e.stopImmediatePropagation();
            });
        }
    });
});
