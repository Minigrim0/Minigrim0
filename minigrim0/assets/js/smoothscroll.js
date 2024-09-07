function smoothScroll(hash) {
    setTimeout(() => {
        var target = $(hash);
        target = target.length ? target : $('[name=' + hash.slice(1) + ']');

        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top
            }, 1000, function () {
                var $target = $(target);
                $target.focus();

                if ($target.is(":focus")) {
                    return false;
                } else {
                    $target.attr('tabindex', '-1');
                    $target.focus();
                };
            });
        }
    }, 100);
}
