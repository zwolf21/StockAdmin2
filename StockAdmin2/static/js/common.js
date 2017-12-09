$(function(){

    // search field focusing first
    $('input[name=search]').select()

    // table sorter global
    $(".tablesorter-sortable").tablesorter({
        widgets: ['zebra'],
        widthFixed: true
    })

    //date picker global
    $.datepicker.setDefaults({
            dateFormat: 'yy-mm-dd',
            prevText: '이전 달',
            nextText: '다음 달',
            monthNames: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
            monthNamesShort: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
            dayNames: ['일', '월', '화', '수', '목', '금', '토'],
            dayNamesShort: ['일', '월', '화', '수', '목', '금', '토'],
            dayNamesMin: ['일', '월', '화', '수', '목', '금', '토'],
            showMonthAfterYear: true,
            yearSuffix: '년'
    });

    $('.datepicker').datepicker({
            dateFormat: 'yy-mm-dd',
            local:'euc-kr'
    });
    
    // 일자 범위 선택시 앞뒤 동기화
    $('.datepicker-start, .datepicker-end').change(function(event){

        var isStart = $(this).hasClass('datepicker-start')
        if (isStart) {
            var start = $(this) 
            var end = $(this).parents('form').find('.datepicker-end')
        } else {
            var end = $(this)
            var start = $(this).parents('form').find('.datepicker-start')
        }

        var startDate = start.val()
        var endDate = end.val()
        if (startDate > endDate) {
            if (isStart) {
                end.val(startDate)
            } else {
                start.val(endDate)
            }
        }
        $(this).parents('form').submit()
    })

}) 
    