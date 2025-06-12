

document.addEventListener('DOMContentLoaded', () => {
    const reportTitle = document.getElementById('report-title');
    // Page sections
    const landingPage = document.getElementById('landing-page');
    const uploadPage = document.getElementById('upload-page');
    const resultsPage = document.getElementById('results-page');

    // Buttons
    const startUploadBtn = document.getElementById('start-upload-btn');
    const verifyBtn = document.getElementById('verify-btn');
    const uploadForm = document.getElementById('upload-form');

    // Upload page elements
    const fileInput = document.getElementById('file-input');
    const imagePreview = document.getElementById('image-preview');
    const previewText = document.getElementById('preview-text');

    // Results page elements
    const refIdSpan = document.getElementById('ref-id');
    const analysisDateSpan = document.getElementById('analysis-date');
    const statusSpan = document.getElementById('status');
    const reportDetailsList = document.getElementById('report-details-list');
    const gaugesContainer = document.getElementById('gauges-container');
    const loader = document.getElementById('loader');


    // --- Event Listeners ---

    // 1. Start Upload Process
    startUploadBtn.addEventListener('click', () => {
        switchPage(uploadPage);
    });

    // 2. File Input & Preview
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
                previewText.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    });

    // 3. Form Submission to Backend
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!fileInput.files[0]) {
            alert('Please upload a document first.');
            return;
        }

        setLoading(true);

        const formData = new FormData(uploadForm);
        const docTypeSelect = document.getElementById('doc-type');
        const selectedDocTypeText = docTypeSelect.options[docTypeSelect.selectedIndex].text;

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'An unknown error occurred.');
            }

            const data = await response.json();
            populateResults(data, selectedDocTypeText); 
            switchPage(resultsPage);

        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            setLoading(false);
        }
    });


    // --- Helper Functions ---

    function switchPage(activePage) {
        document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
        activePage.classList.add('active');
    }

    function setLoading(isLoading) {
        if (isLoading) {
            verifyBtn.classList.add('loading');
            verifyBtn.disabled = true;
        } else {
            verifyBtn.classList.remove('loading');
            verifyBtn.disabled = false;
        }
    }

    function populateResults(data,docTypeText) {
        // Populate header
        refIdSpan.textContent = data.documentReference || 'N/A';
        reportTitle.innerHTML = `${docTypeText.toUpperCase()}<br>ANALYSIS REPORT`; // <-- SETS THE DYNAMIC TITLE
        analysisDateSpan.textContent = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
        statusSpan.textContent = data.status || 'UNKNOWN';

        // Clear previous results
        reportDetailsList.innerHTML = '';
        gaugesContainer.innerHTML = '';

        // Group checks for details list
        const detailBlock = document.createElement('div');
        detailBlock.className = 'detail-block';
        const detailTitle = document.createElement('h4');
        detailTitle.textContent = "Analysis Details";
        const detailList = document.createElement('ul');

        data.checks.forEach(check => {
            // Populate details list
            const listItem = document.createElement('li');
            listItem.innerHTML = `<strong>${check.title}:</strong> ${check.reason}`;
            detailList.appendChild(listItem);

            // Populate gauges
            const gaugeWrapper = document.createElement('div');
            gaugeWrapper.className = 'gauge-wrapper';

            const gaugeHTML = `
                <div class="gauge">
                    <div class="gauge-bg"></div>
                    <div class="gauge-fill" style="--gauge-value: ${check.score}"></div>
                </div>
                <div class="gauge-label">${check.title}</div>
            `;
            gaugeWrapper.innerHTML = gaugeHTML;
            gaugesContainer.appendChild(gaugeWrapper);
        });

        detailBlock.appendChild(detailTitle);
        detailBlock.appendChild(detailList);
        reportDetailsList.appendChild(detailBlock);
    }
});