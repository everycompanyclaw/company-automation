#!/usr/bin/env node
/**
 * Instagram Private API - Auto-Poster
 */
const { IgApiClient } = require('instagram-private-api');
const fs = require('fs');
const os = require('os');

const ig = new IgApiClient();

// Read from temp file (created by shell)
const credsFile = os.homedir() + '/.ig_creds';
let USERNAME = 'everycompanyclaw';
let PASSWORD = '';

try {
    if (fs.existsSync(credsFile)) {
        const creds = fs.readFileSync(credsFile, 'utf8').trim();
        PASSWORD = creds;
    }
} catch(e) {}

const POST_CAPTION = `🧵 20 Python自動化腳本｜幫你慳10+粒鐘

由Email提取器、檔案整理器、發票生成器...
全部已經寫好，等你去用！

💰 $79 = 永久使用

#python #automation #hkig #香港 #startup #indiehacker`;

const IMAGE_PATH = '/Users/macbookpro/Downloads/post.jpg';

async function login() {
    console.log("🔐 Logging in...");
    ig.state.generateDevice(USERNAME);
    await ig.account.login(USERNAME, PASSWORD);
    console.log("✅ Logged in!");
}

async function post() {
    if (!fs.existsSync(IMAGE_PATH)) {
        console.log("❌ No image found");
        return;
    }
    
    console.log("📸 Posting...");
    const imageBuffer = fs.readFileSync(IMAGE_PATH);
    const result = await ig.publish.photo({
        file: imageBuffer,
        caption: POST_CAPTION
    });
    console.log("✅ Posted! ID:", result.media.pk);
}

async function main() {
    if (!PASSWORD) {
        console.log("❌ No password. Set with: echo 'password' > ~/.ig_creds");
        return;
    }
    await login();
    await post();
    console.log("🎉 Done!");
}

main().catch(e => console.log("Error:", e.message));
