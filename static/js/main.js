$(document).ready(function(){
    //Mobile menu toggle
    if ($('.navbar-burger').length) {
        $('.navbar-burger').on("click", function(){

            var menu_id = $(this).attr('data-target');
            $(this).toggleClass('is-active');
            $("#"+menu_id).toggleClass('is-active');
            $('.navbar.is-light').toggleClass('is-dark-mobile')
        });
    }
    //Animate left hamburger icon and open sidebar
    $('.menu-icon-trigger').click(function(e){
        e.preventDefault();
        $('.menu-icon-wrapper').toggleClass('open');
        $('.sidebar').toggleClass('is-active');
    });

    const bulmaCollapsibleInstances = bulmaCollapsible.attach('.is-collapsible');
    // Loop into instances
    bulmaCollapsibleInstances.forEach(bulmaCollapsibleInstance => {
        // Check if current state is collapsed or not
        bulmaCollapsibleInstance.collapsed();
    });
})