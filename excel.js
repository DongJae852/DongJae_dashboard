const excel = {
    downloadTemplate() {
        const data = [
            ['일자', '매장코드', '항목명', '값'],
            ['2026-01-05', 'S001', '박스수량', '10'],
            ['2026-01-05', 'S001', '전달품목', '원두 A'],
        ];
        const ws = XLSX.utils.aoa_to_sheet(data);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Upload_Template");

        /* generate array buffer */
        const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });

        /* create blob and download link */
        const blob = new Blob([wbout], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "Antigravity_Upload_Template.xlsx";
        document.body.appendChild(a);
        a.click();

        setTimeout(() => {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    },

    handleUpload(input) {
        const file = input.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            const jsonData = XLSX.utils.sheet_to_json(worksheet);

            this.processUploadData(jsonData);
            input.value = ''; // Reset
            ui.render(); // Refresh UI
        };
        reader.readAsArrayBuffer(file);
    },

    processUploadData(data) {
        // Expected columns: 일자, 매장코드, 항목명, 값
        data.forEach(row => {
            const date = row['일자'];
            const code = row['매장코드'];
            const fieldMap = {
                '박스수량': 'boxQty',
                '전달품목': 'deliveryItems',
                '본사수거': 'hqCollect',
                '체크사항': 'checkNotes',
                '출고수량': 'outQty'
            };
            const field = fieldMap[row['항목명']];
            const value = row['값'];

            if (date && code && field) {
                // Rule 4: Accumulate if already exists
                const existing = storage.getInputs(date, code)[field] || '';
                const newValue = existing ? `${existing} | ${value}` : value;
                storage.saveInput(date, code, field, newValue);
            }
        });
        alert('엑셀 상향이 완료되었습니다.');
    }
};
