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
        showNotification("Click outside the preview box to exit from preview mode.")
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

/**
 * @returns {Array} array of links
 */
const getAllLinks = () => {
    const files = document.getElementsByClassName("fileItem");
    let links = [];

    for (let a of files) {
        links.push(a.href)
    }

    return links;
}

const copyAllLinks = () => {
    let links = getAllLinks();    

    links = links.join("\n");   
    
    const copyText = async () => {
        try {
            await navigator.clipboard.writeText(links);
        } catch (err) {
            fallbackCopy(links);
        }
    };

    const fallbackCopy = (links) => {
        const textArea = document.createElement("textarea");
        textArea.value = links;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand("copy");
        document.body.removeChild(textArea);
    };

    copyText();

    showNotification("Links copied successfully.");
}

const showNotification = (message) => {
    $(".notifContainer p").text(message)
    $(".notifContainer").addClass("show")
    setTimeout(() => {
        $(".notifContainer").removeClass("show")
    }, 4000)
}