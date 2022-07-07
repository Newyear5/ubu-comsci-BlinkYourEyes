
    let constraintObj = { 
        audio: false, 
        video: {
          width: { min: 640, ideal: 1280, max: 1920 },
          height: { min: 480, ideal: 720, max: 1080 } 
        } 
    };
    let start_button = document.getElementById('btnStart');
    let stop_button = document.getElementById('btnStop');
    let video = document.getElementById('vid1');
    let download_link = document.getElementById('download-video');
    let download_link_button = document.getElementById('download-link');
    let camera_stream = null;
    let media_recorder = null;
    let blobs_recorded = [];
  


    start_button.addEventListener('click', async function() {
    camera_stream = await navigator.mediaDevices.getUserMedia(constraintObj);
	  video.srcObject = camera_stream;
    const tracks = camera_stream.getTracks();
    video.play();

    // set MIME type of recording as video/webm
    media_recorder = new MediaRecorder(camera_stream,{
      mimeType: 'video/webm'
     });
    
    
    // event : new recorded video blob available 
    media_recorder.addEventListener('dataavailable', function(e) {
		  blobs_recorded.push(e.data);
    });

    media_recorder.start();
    // event : recording stopped & all blobs sent
    media_recorder.addEventListener('stop', function() {
    	// create local object URL from the recorded video blobs
    	let video_local = URL.createObjectURL(new Blob(blobs_recorded, { type: 'video/webm;' }));
    	download_link.href = video_local;
      video.pause();
      tracks[0].stop();
      video.srcObject=null;      
    });
});

stop_button.addEventListener('click', function() {
	media_recorder.stop();
  download_link_button.style.display = "block";
});


