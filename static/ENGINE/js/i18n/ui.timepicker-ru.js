/* Russian (UTF-8) initialisation for the jQuery UI date picker plugin. */
/* Written by Andrew Stromnov (stromnov@gmail.com). */ 
jQuery(function($){
    $.timepicker.regional['ru'] = {
        timeOnlyTitle: '�������� �����',
        timeText: '�����',
        hourText: '����',
        minuteText: '������',
        secondText: '�������',
        currentText: '������',
        closeText: '�������',
        ampm: false
    };
    $.timepicker.setDefaults($.timepicker.regional['ru']);
});