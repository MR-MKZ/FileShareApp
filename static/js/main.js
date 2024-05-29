$(() => {

    // Change current drive function
    $("#drivesList").on('change',function () {
        window.location.href = `/chdir/${$(this).val()}`
    })
})