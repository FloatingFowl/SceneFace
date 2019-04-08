var index = (function () {

	var onload = function (ctx, next) {
		console.log("Onload claled");
		//draw();
        Dropzone.options.videoDropzone = {
          url: '/upload_video',
          maxFiles: 1,
          accept: function(file, done) {
            console.log("uploaded");
            done();
          },
          init: function() {
            this.on("maxfilesexceeded", function(file){
                alert("No more files please!");
            });
            this.on('success', function() {
                $("#final-button").show()
            });
          }
        };
    }

	var ret = {};
    //ret.draw = draw;
	ret.onload = onload;
	return ret;

})();

function reset(){
    $('.dropzone')[0].dropzone.files.forEach(function(file) { 
      file.previewElement.remove(); 
    });
}

function prepareKNN(){
    $.ajax({
        type: "POST",
        url: "/prepareKNN",
        success: function (response) {
            console.log("Done")
        },
        async: false,
    });
}

function detectFaces(){
    $.ajax({
        method: "POST",
        url: '/detect_faces',
        success: function (response) {
            $("#video-dropzone").hide();
            $('#video-loc source').attr('src', '/static/video/final.mp4');
            $('#video-loc').show();
            $('#video-loc').load();
        },
        async: false,
    });
}
