

function addShop(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/addgoods/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {

            $('#num_' + goods_id).html(msg.c_num)
        },
        error:function (msg) {
            alert('请求错误')
        }
        
    })
}


function subShop(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/subgoods/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {

            $('#num_' + goods_id).html(msg.c_num)
        },
        error:function (msg) {
            alert('请求错误')
        }

    })
}