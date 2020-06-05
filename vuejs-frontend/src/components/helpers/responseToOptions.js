export default function (text, value){
    let res = []
    if(text.length !== value.length){
        return -1;
    }
    for(let i = 0; i < text.length; i++){
        res.push({
            text : text[i],
            value : value[i]
        });
    }
    return res;

}