$(document).ready(function() {
    let num_photos_printed = -1;
    function fetchPhotosPrinted() {
        $.ajax({
            type: "GET",
            url: "/get_photos_printed",
            success: function (response) {
                file_count = response.file_count
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
    fetchPhotosPrinted();
    setInterval(fetchPhotosPrinted, 60000);
});
