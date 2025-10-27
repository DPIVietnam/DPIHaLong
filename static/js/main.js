$(document).ready(function() {

    function get_today() {
        $.ajax({
            type: "GET",
            url: "/get_today",
            success: function(response) {
                $('#today').html('Ngày: ' + response.today)
            }
        })
    }
    get_today()

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
                    $('#photos_printed_ht').html(response.file_count + ' photos')
                    $('#photo_standard').html(response.file_stand)
                    $('#photo_full').html(response.file_full)
                    $('#photo_extra').html(response.file_extra)
                    $('#photo_customer').html(response.file_customer)
                    let total_money = Number(response.file_stand)*300000 + Number(response.file_full)*440000 + Number(response.file_extra)*80000
                    $('#total_money').html(new Intl.NumberFormat('de-DE').format(total_money) + ' VNĐ')
                }
                else {
                    alert('error')
                }
            }
        });
    }

    // fetchPhotosPrinted()
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

    // setInterval(fetchPhotosPrinted, 120000)
    setInterval(fetchPhotosPrintedHt, 120000)
});
