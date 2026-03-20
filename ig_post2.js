#!/usr/bin/env node
/**
 * Instagram Private API - Try alternative upload
 */
const { IgApiClient } = require('instagram-private-api');
const fs = require('fs');
const os = require('os');

const ig = new IgApiClient();

let PASSWORD = '';
try {
    PASSWORD = fs.readFileSync(os.homedir() + '/.ig_creds', 'utf8').trim();
} catch(e) {}

const USERNAME = 'everycompanyclaw';
const POST_CAPTION = `🧵 20 Python自動化腳本｜幫你慳10+粒鐘

💰 $79
#python #automation #hkig`;

const IMAGE_PATH = '/Users/macbookpro/Downloads/post.png';

async function login() {
    ig.state.generateDevice(USERNAME);
    await ig.account.login(USERNAME, PASSWORD);
    console.log("✅ Logged in!");
}

async function post() {
    console.log("📸 Posting...");
    
    // Try with media config
    const imageBuffer = fs.readFileSync(IMAGE_PATH);
    
    try {
        const result = await ig.publish.photo({
            file: imageBuffer,
            caption: POST_CAPTION,
    });
        console.log("✅ Posted!", result.media.pk);
    } catch(e) {
        console.log("Error:", e.message);
        
        // Try alternative method
        console.log("Trying alternative...");
        const media = await ig.media.upload({
            uploadId: Date.now().toString(),
            file: imageBuffer,
            isDirect: false,
        });
        console.log("✅ Alt posted!");
    }
}

login().then(post).catch(e => console.log("Final error:", e.message));
