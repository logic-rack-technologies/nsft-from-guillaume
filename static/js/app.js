/*
Template Name: Ordo
Author: Noésis Software Technologies
Version: 3.0.0
Website: https://nsft.fr/
Contact: g.barbat@nsft.fr
File: Custom Js init
*/
(function($) {
    "use strict";

    var language = localStorage.getItem("language");
    // Default Language
    var default_lang = "en";

    function setLanguage(lang) {
        if (document.getElementById("header-lang-img")) {
            if (lang == "en") {
                document.getElementById("header-lang-img").src =
                    "/static/images/flags/us.jpg";
            } else if (lang == "fr") {
                document.getElementById("header-lang-img").src =
                    "/static/images/flags/french.jpg";
            }
            sessionStorage.getItem('language', lang);
            if (lang) {
                $.ajax({
                    url: `/set-language/?language=${lang}`,
                    dataType: 'json',
                    method: 'GET',
                    success: function(response) {
                        if (lang == 'en') {
                            window.location = window.location.toString().replace('fr', 'en');
                        } else {
                            window.location = window.location.toString().replace('en', 'fr');
                        }
                    }
                    // success: function(response) {
                    //     if (lang == 'en') {
                    //         window.location = window.location.toString().replace('.fr/fr', '.fr/en');
                    //     } else {
                    //         window.location = window.location.toString().replace('.fr/en', '.fr/fr');
                    //     }
                    // }
                });
            }
        }
    }

    function initMetisMenu() {
        //metis menu
        $("#side-menu").metisMenu();
    }

    function initLeftMenuCollapse() {
        $("#vertical-menu-btn").on("click", function(event) {
            event.preventDefault();
            $("body").toggleClass("sidebar-enable");
            if ($(window).width() >= 992) {
                $("body").toggleClass("vertical-collpsed");
            } else {
                $("body").removeClass("vertical-collpsed");
            }
        });
    }

    function initActiveMenu() {
        // === following js will activate the menu in left side bar based on url ====
        $(".nav-item a").each(function() {
            var pageUrl = window.location.href.split(/[?#]/)[0];
            if (this.href == pageUrl) {
                $(this).closest('.nav-link').addClass("active");

            }
        });
    }

    function initMenuItemScroll() {
        // focus active menu in left sidebar
        $(document).ready(function() {
            if (
                $("#sidebar-menu").length > 0 &&
                $("#sidebar-menu .mm-active .active").length > 0
            ) {
                var activeMenu = $("#sidebar-menu .mm-active .active").offset().top;
                if (activeMenu > 300) {
                    activeMenu = activeMenu - 300;
                    $(".vertical-menu .simplebar-content-wrapper").animate({ scrollTop: activeMenu },
                        "slow"
                    );
                }
            }
        });
    }

    function initHoriMenuActive() {
        $(".navbar-nav a").each(function() {
            var pageUrl = window.location.href.split(/[?#]/)[0];
            if (this.href == pageUrl) {
                $(this).addClass("active");
                $(this).parent().addClass("active");
                $(this).parent().parent().addClass("active");
                $(this).parent().parent().parent().addClass("active");
                $(this).parent().parent().parent().parent().addClass("active");
                $(this).parent().parent().parent().parent().parent().addClass("active");
                $(this)
                    .parent()
                    .parent()
                    .parent()
                    .parent()
                    .parent()
                    .parent()
                    .addClass("active");
            }
        });
        $("a.stepper-process").each(function(e) {
            var stepper = window.location.href.split(/[?#]/)[0];
            if (this.href == stepper) {
                $(`.${this.id}`).addClass("bg-warning");
            }
        });
    }
    function initComponents() {
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl)
            });

            var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
            var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
                return new bootstrap.Popover(popoverTriggerEl)
            });

            var offcanvasElementList = [].slice.call(document.querySelectorAll('.offcanvas'))
            var offcanvasList = offcanvasElementList.map(function (offcanvasEl) {
                return new bootstrap.Offcanvas(offcanvasEl)
            })
        }

    function initRightSidebar() {
        // right side-bar toggle
        $(".right-bar-toggle").on("click", function(e) {
            $("body").toggleClass("right-bar-enabled");
        });

        $(document).on("click", "body", function(e) {
            if ($(e.target).closest(".right-bar-toggle, .right-bar").length > 0) {
                return;
            }

            $("body").removeClass("right-bar-enabled");
            return;
        });
    }

    function initDropdownMenu() {
        if (document.getElementById("topnav-menu-content")) {
            var elements = document
                .getElementById("topnav-menu-content")
                .getElementsByTagName("a");
            for (var i = 0, len = elements.length; i < len; i++) {
                elements[i].onclick = function(elem) {
                    if (elem.target.getAttribute("href") === "#") {
                        elem.target.parentElement.classList.toggle("active");
                        elem.target.nextElementSibling.classList.toggle("show");
                    }
                };
            }
            window.addEventListener("resize", updateMenu);
        }
    }

    function updateMenu() {
        var elements = document
            .getElementById("topnav-menu-content")
            .getElementsByTagName("a");
        for (var i = 0, len = elements.length; i < len; i++) {
            if (
                elements[i].parentElement.getAttribute("class") ===
                "nav-item dropdown active"
            ) {
                elements[i].parentElement.classList.remove("active");
                elements[i].nextElementSibling.classList.remove("show");
            }
        }
    }

    function initComponents() {
        var tooltipTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        var popoverTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="popover"]')
        );
        var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    function initPreloader() {
        $(window).on("load", function() {
            $("#status").fadeOut();
            $("#preloader").delay(350).fadeOut("slow");
        });
    }

    function initLanguage() {
        // Auto Loader
        $(".language").on("click", function(e) {
            setLanguage($(this).attr("data-lang"));
        });
    }

    function initCheckAll() {
        $("#checkAll").on("change", function() {
            $(".table-check .form-check-input").prop(
                "checked",
                $(this).prop("checked")
            );
        });
        $(".table-check .form-check-input").change(function() {
            if (
                $(".table-check .form-check-input:checked").length ==
                $(".table-check .form-check-input").length
            ) {
                $("#checkAll").prop("checked", true);
            } else {
                $("#checkAll").prop("checked", false);
            }
        });
    }

    function init() {
        initRightSidebar();
        initMetisMenu();
        initLeftMenuCollapse();
        initActiveMenu();
        initMenuItemScroll();
        initHoriMenuActive();
        initDropdownMenu();
        initComponents();
        initLanguage();
        initPreloader();
        initCheckAll();
    }

    init();
})(jQuery);