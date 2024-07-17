import Uppy from '@uppy/core'
import Webcam from '@uppy/webcam'
import Dashboard from '@uppy/dashboard'
import XHRUpload from '@uppy/xhr-upload'

import '@uppy/core/dist/style.css'
import '@uppy/webcam/dist/style.css'
import '@uppy/dashboard/dist/style.css'


const uppy = new Uppy({
  debug: false,
  autoProceed: false,
  restrictions: {
    maxFileSize: 1000000, // 10MB
    maxNumberOfFiles: 10,
    minNumberOfFiles: 1,
    allowedFileTypes: ['image/*'] // 仅允许图片文件
  }
})

uppy.use(Webcam)
uppy.use(Dashboard, {
  inline: true,
  target: '#drag-drop-area',
  plugins: ['Webcam'],
})


uppy.use(XHRUpload, {
  endpoint: '/qrcode/',
  formData: true,
  fieldName: 'file'
})

uppy.on('upload-success', (file, response) => {
  if (response.status === 200) {
    const responseData = response.body;
    if (responseData.code == 0 ){
        $('#fail_alert').show();
        $('#fail_detail').text("No Secret Code found From Upload Image");
        setTimeout(function() {$('#fail_alert').hide();}, 2000); // 2 seconds

    } else {
        $('#id_app_two_fa').val(responseData.qrcode);
        $('#success_alert').show();
        $('#success_detail').text("Found Secret Code From Upload Image.");
        setTimeout(function() {$('#success_alert').hide();}, 2000); // 2 seconds
    }
    //console.log('Upload successful!', responseData);
    //alert(responseData.qrcode);
  } else {
      $('#fail_alert').show();
      $('#fail_detail').text("No Secret Code found From Upload Image");
      setTimeout(function() {$('#fail_alert').hide();}, 2000); // 2 seconds
  }
});


