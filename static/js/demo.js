/**
 * Created by Becario on 20/04/2015.
 */
$(function(){
    $('#menu a[href*="' + location.pathname.split("/")[1] + '"][class!="noactivo"]').addClass('activo');
});
