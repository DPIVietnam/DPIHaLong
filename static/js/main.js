$(document).ready(function() {
    $('#checkNumQr').on('click', function(){
        var numQr = $('#input_qr').val()
        console.log(numQr)
        $.ajax({
            type: "POST",
            url: "/show_qrcode",
            data: JSON.stringify({numQr: numQr}),
            contentType: 'application/json',
            success: function (response) {
                if(response.result !== false) {
                    $('#qrcode').attr('src', response.path)
                    $('#qrcode').css('opacity', 1)
                }
                else {
                    alert('Error generating QR code');
                }
            }
        });
    })

    $('#input_qr').keydown(function(){
        $('#qrcode').css('opacity', 0)
        $('#qrcode').attr('src', '/static/images/coaster.png')
    })
    let num_photos_printed = -1;
    function fetchPhotosPrinted() {
        $.ajax({
            type: "GET",
            url: "/get_photos_printed",
            success: function (response) {
                file_count = response.file_count
                console.log(response.file_count);
                
                $('#today').html('Ngày: ' + response.today)
                if(file_count != num_photos_printed) {
                    $('#photos_printed').html(file_count + ' Hình Ảnh')
                    var cost = file_count * 150000
                    $('#total_cost').html(new Intl.NumberFormat('de-DE').format(cost) + ' VNĐ')
                }
                else {
                    alert('error')
                }
            }
        });
    }

    function fetchPhotosPrintedHt() {
        $.ajax({
            type: "GET",
            url: "/get_photos_printed_ht",
            success: function (response) {
                console.log(response.file_customer);
                
                if(response.file_count != num_photos_printed) {
                    $('#photos_printed_ht').html(response.file_count + ' Hình Ảnh')
                    $('#photo_standard').html(response.file_stand)
                    $('#photo_full').html(response.file_full)
                    $('#photo_extra').html(response.file_extra)
                    $('#photo_customer').html(response.file_customer)
                }
                else {
                    alert('error')
                }
            }
        });
    }

    fetchPhotosPrinted()
    fetchPhotosPrintedHt()

    const $tabButton1 = $('#tab-coaster');
    const $tabButton2 = $('#tab-honthom')
    const $tabPane1 = $('#tab1');
    const $tabPane2 = $('#tab2');


    // Lắng nghe sự kiện click trên mỗi tab
    $tabButton1.on('click', function() {
        console.log(123);
        
        // Loại bỏ class "active" của tất cả các tab
        $tabButton2.removeClass('active');
        $tabPane2.removeClass('active');

        // Thêm class "active" cho tab và nội dung tab được chọn
        $(this).addClass('active');
        $tabPane1.addClass('active')
    });

    $tabButton2.on('click', function() {
        console.log(123);
        
        // Loại bỏ class "active" của tất cả các tab
        $tabButton1.removeClass('active');
        $tabPane1.removeClass('active');

        // Thêm class "active" cho tab và nội dung tab được chọn
        $(this).addClass('active');
        $tabPane2.addClass('active')
    });

    function checkImage() {
        let imgNumber = $('#imgNumber').val()
        $.ajax({
            url: '/check_image',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({img_number: imgNumber}),
            success: function (response) {
                if (response.path) {
                    $("#imageContainer, #result").empty()
                    $('#result').text('Hình ảnh được tìm thấy !')
                    $("#imageContainer").append("<img src='" + response.path + "'" + 'width="100%">')
                } else {
                    $("#imageContainer, #result").empty()
                    $('#result').text('Hình ảnh không được tìm thấy !')
                }
            }
        })
    }

    function check_dir() {
        let lastFiveDigits = $("#lastFiveDigits").val();
        console.log(lastFiveDigits);
        

        $.ajax({
            type: "POST",
            url: "/find_directory",
            data: {last_five_digits: lastFiveDigits},
            success: function (response) {
                $("#check_dir_img, #result1").empty()
                $('#result1').text(response.msg)
                $("#check_dir_img").append("<img src='" + response.file_path + "'" + 'width="100%">')
            }
        })
    }

    $("#imgNumber").keypress(function(event) {
        if (event.keyCode === 13) {
            checkImage()
        }
    })
    $("#lastFiveDigits").keypress(function(event) {
        if (event.keyCode === 13) {
            check_dir()
        }
    })

    $("#add_more_images").click(function () {
        // Đổi màu nút thành xanh lá và thông báo đang xử lý
        $(this).css('background-color', 'green');
        $(this).text('Nào nào, đừng như nước sôi đổ vô trứng cút');

        // Gửi yêu cầu POST đến /process
        $.ajax({
            type: "POST",
            url: "/process",
            success: function (response) {
                if (response.result === true) {
                    $("#add_more_images").css('background-color', '');

                    // Thêm thông báo vào trang web
                    var notification = $('<div class="alert alert-success"  style="font-size: 30px;color: black;" role="alert">Đã hoàn thành thêm ảnh điện tử</div>');
                    $("#content").append(notification);

                    // Tự động ẩn thông báo sau 3 giây
                    setTimeout(function () {
                        notification.fadeOut('slow', function () {
                            $(this).remove();
                        });
                    }, 3000);
                    $('#add_more_images').text('Thêm ảnh điện tử');
                } else {
                    // Đã có ảnh trong thư mục
                    console.log(response.result);
                    $("#add_more_images").css('background-color', '');

                    // Thêm thông báo vào trang web
                    var notification1 = $('<div class="alert alert-danger"  style="font-size: 30px;color: black;" role="alert">Giống mợ ba Huyền quá, thêm rồi, thêm quàiiiii, yêu Khang rồi "nú nẫn" hà </div>');
                    $("#content").append(notification1);

                    // Tự động ẩn thông báo sau 3 giây
                    setTimeout(function () {
                        notification1.fadeOut('slow', function () {
                            $(this).remove();
                        });
                    }, 3000);
                    $('#add_more_images').text('Thêm ảnh điện tử');

                }
            }
        })
    });

    function check_image_error() {
        let imgNumber = $('#err_imgNumber').val()
        $.ajax({
            url: '/check_image_error',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({img_number: imgNumber}),
            success: function (response) {
                if (response.result !== false) {
                    console.log(response.path);
                    
                    $("#err_imageContainer, #err_result, #err_result1, #err_imageContainer1").empty()
                    $('#err_result').text('Hình ảnh được tìm thấy !').css('color', 'black')
                    $("#err_imageContainer").append("<img src='" + response.path + "'" + 'width="100%">')
                    $('#err_result1').text('Ảnh sau khi sửa -> KHÔNG SỬA ĐƯỢC THÌ QUA SỬA TAY NHÉ! :))').css('font-weight', 'bold')
                    // $("#err_imageContainer1").append("<img src='" + response.raw_path + "'" + 'width="100%">')
                } else {
                    $("#err_imageContainer").html("<img id='img_error_notify' src='" + "static/temp/container/error_notify.png" + "'" + 'width="100%">')
                    $("#err_result, #err_imageContainer1").empty()
                    $('#err_result').text('CHẮC ĂN ĐẤM QUÁ ! SAI SỐ RỒI HUYỀN ƠI !').css('color', 'red')
                }
            }
        })
    }

    function remove_background (firstNum, lastNum) {
        // Đổi màu nút thành xanh lá khi bắt đầu xử lý
       $(this).css('background-color', 'green');

       // Hiển thị thông báo "Đang xử lý..."
       $(this).text('Từ từ, để tách, khó vcl, đừng hối');

       // Gửi yêu cầu POST đến /process
        $.ajax({
            url: '/remove_bg',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({firstNum: firstNum, lastNum: lastNum}),
            success: function (response) {
                if (response.result === true) {
                   $("#remove_bg").css('background-color', '');
                   // Thêm thông báo vào trang web
                   var notification2 = $('<div class="alert alert-success"  style="font-size: 30px;color: black;" role="alert">Đã tách nền hoàn thành</div>');
                   $("#content_rbg").append(notification2);
                   // Tự động ẩn thông báo sau 3 giây
                   setTimeout(function () {
                       notification2.fadeOut('slow', function () {
                           $(this).remove();
                       });
                   }, 2000);
                   $("#err_imageContainer1").html("<img src='" + response.img_after_edit + "'" + 'width="100%">');
                   $('#remove_bg').text('Tách nền');
               } else {
                   alert('Tách nền thất bại')
               }
            }
        })
    }

    $("#err_imgNumber").keypress(function(event) {
        if (event.keyCode === 13) {
            check_image_error()
        }
    })

    $("#find_img").on("click", function() {
        check_image_error()
    })

    $("#remove_bg").click(function () {
        remove_background(107, 10000)
        $("#edit_try").css("display", "block");
        $("#reload_img").css("display", "block");
    });

    $("reload_img").on("click", function() {
        $.ajax({
            url: '/reload_img',
            type: 'POST',
            contentType: 'application/json',
            success: function(response) {
                $('#err_imageConatiner1').html("<img src='" + response.img_path + "'" + 'width="100%"');
            }
        })
    })

    setInterval(fetchPhotosPrinted, 60000)
    setInterval(fetchPhotosPrintedHt, 120000)
});
