import React, { Component,Fragment } from 'react';
import AWS from 'aws-sdk';

const $ = window.$;
var bucketName = "serverless-object-detection";
var bucketRegion = "us-east-1";
var IdentityPoolId = "us-east-1:b4bd7b63-d1ac-4a26-a8e8-177fd035a638";
 
AWS.config.update({
    region: bucketRegion,
    credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: IdentityPoolId
    })
});

    var s3 = new AWS.S3({
        apiVersion: '2006-03-01',
        params: {Bucket: bucketName}
    });


export default class Upload extends Component {
    constructor(){
        super();
    }
    


    s3upload() {  
        
        var files = document.getElementById('fileUpload').files;
        if (files) 
        {
            var file = files[0];
            var fileName = file.name;
            var filePath = fileName;
            var fileUrl = 'https://' + bucketRegion + '.amazonaws.com/' +  filePath;

    
            s3.upload({
                            Key: filePath,
                            Body: file,
                            ACL: 'public-read'
                        }, function(data) {
                            alert('Successfully Uploaded!');
                        }).on('httpUploadProgress', function (progress) {
                            var uploaded = parseInt((progress.loaded * 100) / progress.total);
                            $("progress").attr('value', uploaded);
                        });$(document).on('change', '.custom-file-input', function (event) {
                            $(this).next('.custom-file-label').html(event.target.files[0].name);
                        })
                        ;
                       
        }
    };




render(){
    
    return (
        <Fragment>
       <form>
       {this.props.auth.isAuthenticated && this.props.auth.user && (
       <div className="container mt-4">
            <h1 className="display-4 text-center mb-4">
            <i className="fa-react"/><b>Select image to upload</b></h1>

            


            
            <div className="container mt-4">
            <input type="file" class="custom-file-input" id="fileUpload"/>
            <label class="custom-file-label" htmlFor="fileUpload">Choose file</label></div>


            <div className="container mt-4">
            <button type="button" className="btn btn-primary btn-xl btn-block float-right" onClick={this.s3upload}>Upload</button></div>
            <progress max='100' value='0'/>

            


            
       
            
              </div>
       )}
              </form>
        </Fragment>
    );
}
}





