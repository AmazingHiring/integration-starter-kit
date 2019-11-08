const INTEGRATION_SERVER_URL = 'http://localhost:8888/save_profile/';


var urlRegEx = /https:\/\/search\.amazinghiring\.com\/profiles\/([0-9]+).*$/;

chrome.tabs.onActivated.addListener(function(activeInfo) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        var activeTab = tabs[0];

        if (urlRegEx.test(activeTab.url)) {
            chrome.browserAction.enable(activeTab.id);
        } else {
            chrome.browserAction.disable(activeTab.id);
        }
   
     });
});

chrome.browserAction.onClicked.addListener(function(activeTab) {
    if (urlRegEx.test(activeTab.url)) {
        var profile_id = activeTab.url.match(urlRegEx)[1];
        var xhr = new XMLHttpRequest();
        xhr.open('GET', INTEGRATION_SERVER_URL + profile_id + '/', true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                console.log('saved');
            }
        }
        xhr.send();
    }
})