import CryptoJS from 'crypto-js'

export {
    encrypted,
    decrypted
}

function encrypted(key, text){
    const encrypted = CryptoJS.TripleDES.encrypt(text, CryptoJS.enc.Utf8.parse(key), 
    { 
        mode: CryptoJS.mode.ECB,  
        padding: CryptoJS.pad.Pkcs7  
    });

    return encrypted.toString(); // 返回加密后的字符串
}



function decrypted(key, text) {

    const decrypted = CryptoJS.TripleDES.decrypt(text,CryptoJS.enc.Utf8.parse(key), { 
        mode: CryptoJS.mode.ECB,  
        padding: CryptoJS.pad.Pkcs7 
    }).toString(CryptoJS.enc.Utf8);

    return decrypted // 返回解密后的字符串
}