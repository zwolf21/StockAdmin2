$(function(){
    $('table.grid-table input[type=text], table.grid-table input[type=number]').keydown(function(event){
        var cell = $(this)
        var row = cell.parents('tr')
        var nrow = row.parent().children('tr').index(row)
        var keyCode = event.keyCode

        // console.log(keyCode)
        switch(keyCode){
            case 32:
                var max = $(this).attr('max')
                $(this).val(max)
                break;
            case 37: case 39:
            //     var rowInputs = row.children('td').children('input[type=number]')
            //     c = rowInputs
            //     i = cell
            //     var idx = rowInputs.index(cell)
            //     idx = keyCode == 37 ? Math.max(idx -1, 0) : Math.min(idx+1, rowInputs.length-1)
            //     var target = rowInputs[idx]
            //     target.focus()
            //     target.select()
                console.log('37, 39')
                return true
            case 38: case 40:
                var rowInputs = row.children('td').children('input[type=number]')
                var colIdx = rowInputs.index(cell)
                if(keyCode == 38) {
                    if (nrow==0) {
                        return false
                    }
                    var prevRow = row.prevAll('tr').first()
                    var prevRowInputs = prevRow.children('td').children('input[type=number]')
                    var target = prevRowInputs[colIdx]
                }else {
                    var nextRow = row.nextAll('tr').first()
                    var nextRowInputs = nextRow.children('td').children('input[type=number]')
                    var target = nextRowInputs[colIdx]
                }
                target.focus()
                return false;
            default:
                return true
        }
    })
})