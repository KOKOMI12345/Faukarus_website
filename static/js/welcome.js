//侧边栏
$(document).ready(function () {
    var sidebar = $('.sidebar');

    // 切换侧边栏
    $('.btn-toggle-sidebar').click(function () {
        sidebar.toggleClass('open');
    });

    // 鼠标离开侧边栏时自动隐藏
    sidebar.mouseleave(function () {
        sidebar.removeClass('open');
    });
});
//头像的更新及保存
$('#id_file').change(function () {
    //取到文件对象
    var file = $('#id_file')[0].files[0]
    //生成一个文件阅读器对象
    var filereader = new FileReader()
    //把文件读到filereader对象
    filereader.readAsDataURL(file)
    filereader.onload = function () {
        $('#id_img').attr('src', filereader.result)
    }
    var formdata = new FormData();
    formdata.append('file', file)
    $.ajax({
        url: '/avatar',
        type: 'POST',
        data: formdata,
        contentType: false,
        processData: false,
        success: function (response) {
            // 处理成功响应
            console.log('文件上传成功');
        },
    })

})
//上传图片
$('#image_file').change(function () {
    //取到文件对象
    var file = $('#image_file')[0].files[0]
    //生成一个文件阅读器对象
    var filereader = new FileReader()
    //把文件读到filereader对象
    filereader.readAsDataURL(file)
    filereader.onload = function () {
        $('#image_picture').attr('src', filereader.result)
    }

})

$('#image_upload').click(function () {
    var file = $('#image_file')[0].files[0]
    var formdata = new FormData();
    formdata.append('image', file)
    console.log(formdata)
    $.ajax({
        url: '/upload',
        type: 'post',
        data: formdata,
        contentType: false,
        processData: false,
        success: function (response) {
            // 处理成功响应
            if (response.code == 100) {
                $('#imageModal').modal('hide')
                alert(response.msg)
            } else {
                alert(response.msg)
            }
        },
    })
})

$('#imageModal').on('show.bs.modal', function () {
    $('#image_picture').attr('src', ''); // 清空图片值
});

var id;

function handleClick(index) {
    id = index
}

//向好友发送消息
$('#send_btn').click(function () {
    $.ajax({
        url: '/sendmsg',
        type: 'post',
        data: {
            recive_id: id,
            send_name: '{{ username }}',
            message: $('#message').val()
        },
        success: function (data) {
            if (data.code == 100) {
                $('#messageModal').modal('hide')
                alert(data.msg)

            } else {
                alert('发送失败')
            }
        }
    })
})
$('#messageModal').on('show.bs.modal', function (e) {
    // 清空textarea的值
    $('#message').val('');
});
//查看消息
$('#Mymessage').click(function() {
    $.ajax({
        url: '/message',
        type: 'get',
        success: function(data) {
            // 清空原有消息内容
            $('#modal-body-message').empty();

            // 遍历每条消息数据，并添加到 modal-body 中
            $.each(data.message, function(index, message) {
                var messageItem = $('<p>')
                    .append($('<span>').text(message.sender + ' :'))
                    .append(
                        $('<span>')
                            .css('margin-left', '20px')
                            .text('---' + message.timestamp)
                    )
                    .append($('<br>'))
                    .append($('<span>').text(message.message));

                $('#modal-body-message').append(messageItem);
            });
        }
    })
});

//好友列表
$('#myfriend_list').click(function (){
    $.ajax({
            url: '/friend_list',
    type: 'get',
    success: function(data) {
        // 清空原有数据
        $('#friendList').empty();

        // 遍历每个好友数据，并添加到 friendList 列表中
        $.each(data.page_data, function(index, friend) {
            var listItem = $('<li>')
                .addClass('dropdown')
                .css('color', 'white')
                .css('font-size', '18px')
                .append(
                    $('<a>')
                        .attr('href', '#')
                        .attr('id', friend.id + '_name')
                        .addClass('dropdown-toggle')
                        .attr('data-toggle', 'dropdown')
                        .attr('role', 'button')
                        .attr('aria-haspopup', 'true')
                        .attr('aria-expanded', 'false')
                        .css('color', 'white')
                        .css('text-decoration', 'none')
                        .click(function() {
                            handleClick(friend.id);
                        })
                        .text(friend.user)
                )
                .append(
                    $('<ul>').addClass('dropdown-menu').append(
                        $('<li>').append(
                            $('<a>')
                                .attr('href', '#')
                                .css('color', '#fb7299')
                                .attr('data-toggle', 'modal')
                                .attr('data-target', '#messageModal')
                                .text('发送消息')
                        )
                    )
                );

            $('#friendList').append(listItem);
        });

        // 渲染分页导航
        if (data.total) {
            var pagination = $('<nav>').attr('aria-label', 'Page navigation');
            var paginationList = $('<ul>').addClass('pagination');

            // 添加上一页按钮
            paginationList.append(
                $('<li>').append(
                    $('<a>')
                        .attr('href', '/welcome?page=1')
                        .attr('aria-label', 'Previous')
                        .append($('<span>').attr('aria-hidden', 'true').html('&laquo;'))
                )
            );

            // 循环添加页码按钮
            for (var i = 1; i <= data.total; i++) {
                paginationList.append(
                    $('<li>').append(
                        $('<a>').attr('href', '/welcome?page=' + i).text(i)
                    )
                );
            }

            // 添加下一页按钮
            paginationList.append(
                $('<li>').append(
                    $('<a>')
                        .attr('href', '/welcome?page=' + data.total)
                        .attr('aria-label', 'Next')
                        .append($('<span>').attr('aria-hidden', 'true').html('&raquo;'))
                )
            );

            pagination.append(paginationList);
            $('#friendList').after(pagination);
        }
    }
})
    })

//添加好友
$('#addfriend').click(function () {
    $.ajax({
        url: '/addfriend',
        type: 'post',
        data: {
            friend_name: $('#friendIdInput').val(),
            my_name: '{{ username }}'
        },
        success: function (data) {
            if (data.code == 100) {

                var friendList = $('#friendList');
                friendList.empty();
                $('#addFriendModal').modal('hide')
                alert(data.msg)
                // 添加新的列表项
                $.each(data.friends, function (index, friend) {
                    var listItem = '<li style="color: #fb7299;font-size: 18px" class="dropdown">' +
                        '<a href="#" id="' + friend.user + '_name" class="dropdown-toggle" ' +
                        'data-toggle="dropdown" role="button" aria-haspopup="true" ' +
                        'aria-expanded="false" style="color:#fb7299;text-decoration: none;" ' +
                        'onclick="handleClick(' + friend.id + ')">' +
                        friend.user +
                        '<span class="caret"></span>' +
                        '</a>' +
                        '<ul class="dropdown-menu">' +
                        '<li><a href="#" style="color: #fb7299" data-toggle="modal" data-target="#messageModal">发送消息</a></li>' +
                        '</ul>' +
                        '</li>';

                    friendList.append(listItem);

                });
            } else {
                alert(data.msg);
            }


        }
    })

})

$('#addFriendModal').on('show.bs.modal', function (e) {
    // 清空textarea的值
    $('#friendIdInput').val('');
});
//发布帖子
$("#btn-new-post").click(function() {
    $("#newPostModal").modal("show"); // 显示模态框
});

$('#btn_send_post').click(function (){
    $.ajax({
        url:'/send_posts',
        type:'post',
        data:{
            title:$('#postTitle').val(),
            content:$('#postContent').val()
        },
        success:function (data){
            if(data.code==100){
                alert(data.msg)
                $('#newPostModal').modal('hide');
                location.href = '/welcome'
            }
        }
    })
})