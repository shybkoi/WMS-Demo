/* Russian (UTF-8) initialisation for the jQuery UI date picker plugin. */
/* Written by Andrew Stromnov (stromnov@gmail.com). */ 
jQuery(function($){
    $.timepicker.regional['ru'] = {
        timeOnlyTitle: 'Выберите время',
        timeText: 'Время',
        hourText: 'Часы',
        minuteText: 'Минуты',
        secondText: 'Секунды',
        currentText: 'Сейчас',
        closeText: 'Закрыть',
        ampm: false
    };
    $.timepicker.setDefaults($.timepicker.regional['ru']);
});