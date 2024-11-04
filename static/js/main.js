$(document).ready(function() {
    let num_photos_printed = -1;
    $.ajax({
        type: "GET",
        url: "/get_photos_printed",
        success: function (response) {
            file_count = response.file_count
            if(file_count != num_photos_printed) {
                $('#photos_printed').append(file_count + ' Hình ảnh')
                var cost = file_count * 150000
                $('#total_cost').append(new Intl.NumberFormat('de-DE').format(cost) + ' VNĐ')
            }
            else {
                alert('error')
            }
        }
    });

});
