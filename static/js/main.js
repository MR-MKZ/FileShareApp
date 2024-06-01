$(() => {
    // Change current drive function
    $("#drivesList").on('change', function () {
        window.location.href = `/chdir/${$(this).val()}`
    })

    $(".showPreview").click(function () {
        let fileNameArray = $(this).attr("name").split(".")
        let fileExtension = fileNameArray[fileNameArray.length - 1]
        if (isImage(fileExtension)) {
            $(".Modal img").attr("src", $(this).attr("src"))
            $(".Modal img").attr("alt", $(this).attr("name"))
            $(".Modal img").show()
            $(".backward").fadeIn()
            $(".Modal").fadeIn();
        }
        if (isVideo(fileExtension)) {
            $(".Modal video").attr("src", $(this).attr("src"))
            $(".Modal video").show()
            $(".Modal video").get(0).play()
            $(".backward").fadeIn()
            $(".Modal").fadeIn();
        }
    })

    $(".backward").click(function (){
        $(".Modal video").get(0).pause()
        $(".Modal").fadeOut()
        $(this).fadeOut()
        $(".Modal video").hide()
        $(".Modal img").hide()
    })
})
const imageExtensions = [
    "png",
    "jpg",
    "jpeg",
    "gif"];
const videoExtensions = ["mp4",
    "mkv",
    "avi",
    "flv",
    "webm",
    "wmv"];

const isImage = (extension) => {
  return imageExtensions.indexOf(extension) > -1;
}

const isVideo = (extension) => {
  return videoExtensions.indexOf(extension) > -1;
}