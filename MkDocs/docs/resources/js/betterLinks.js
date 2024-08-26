document$.subscribe(function () {
    $("a").each(function () {
        var $link = $(this);
        if ($link.hasClass("msg")) {
            msg = decodeURIComponent($link.attr("href"));
            if (msg.startsWith("msg:")) {
                msg = msg.substring(4);
            } else if (msg.startsWith("base64:")) {
                msg = atob(msg.substring(7));
            }
            if (msg.startsWith("'") && msg.endsWith("'")) {
                msg = msg.substring(1, msg.length - 1);
            }
            $link.removeAttr("href").attr("hrefmsg", msg);
            $link.on("click", function (e) {
                e.stopImmediatePropagation();
                alert$.next($link.attr("hrefmsg"));
            });
        } else if (!$link.attr("href")) {
            $link.removeAttr("href");
            $link.css("cursor", "auto");
            $link.on("click", function (e) {
                e.stopImmediatePropagation();
            });
        }
    });
});
