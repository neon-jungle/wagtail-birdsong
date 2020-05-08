class CampaignPreviewHandler {
    constructor(form, button) {
        this.form = form;
        this.button = button;
        this.previewURL = button.dataset['action'];
        this.setupListeners();
    }

    setupListeners() {
        this.button.addEventListener('click', (e) => {
            e.preventDefault();
            this.button.classList.remove('icon-view');
            this.button.classList.add('icon-spinner');
            this.showPreview();
        });
    }

    showPreview() {
        // alert(this.previewURL);
        const formData = new FormData(this.form);
        fetch(this.previewURL, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            },
            body: formData
        })
            .then(response => response.json())
            .then(responseJSON => {
                if (responseJSON.success) {
                    alert('doin the preview');
                } else {
                    alert('Your form has missing/incorrect data');
                    // Try to submit the form to show errors?
                }
            })
    }
}


document.addEventListener('DOMContentLoaded', _ => {
    form = document.querySelector('.content form'); // not the best selector
    button = document.querySelector('.campaign-preview');
    if (form && button) {
        new CampaignPreviewHandler(form, button);
    }
});