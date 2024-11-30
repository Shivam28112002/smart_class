function result(){
    var students={
        SHIVAM: {
            math: "95",
            physics: "80",
            literature: "75",
        },
        OBAMA: {
            math: "95",
            physics: "80",
            literature: "75",
        },
        ELON: {
            math: "95",
            physics: "80",
            literature: "75",
        }
    }
    var studentname=document.getElementById('studentname').value;  //It fetches the value entered into an input field
    var input=studentname.toUpperCase();  //Converts the input into uppercase using to match the in input
    var definition= students[input];
    var output= document.getElementById("output");

    if(definition==undefined){
        output.innerHTML=`<hr> There is no information about this student. <hr>`;
    }
    else{
        output.innerHTML= `<hr> Maths Score is ${definition.math}. <hr> Physics Score is ${definition.physics}. <hr> Literature Score is ${definition.literature}.<hr>`
    }
}