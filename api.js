const api = {
    CONFIG: {
        SPREADSHEET_ID: '1iImYZb5i9F810ARDycWaBUNiuB_D4qjqs0W1zF_DuNk',
        API_KEY: 'AIzaSyDLGtTFkkh2x1vtp5Xf0JfLD3nclJwow_U',
        RANGE: 'A2:G500' // Starts from A2 to skip headers
    },

    async fetchShops() {
        const url = `https://sheets.googleapis.com/v4/spreadsheets/${this.CONFIG.SPREADSHEET_ID}/values/${encodeURIComponent(this.CONFIG.RANGE)}?key=${this.CONFIG.API_KEY}`;

        try {
            const response = await fetch(url);
            const data = await response.json();

            if (!data.values) {
                console.error('No data found in sheet.');
                return [];
            }

            // Map columns: [매장코드, 매장명, 납품코드, 코스, 순서, 영업시간, 주소]
            return data.values.map(row => ({
                code: row[2] || '', // 납품코드 (using this as the unique ID for deliveries as per prompt [2])
                originalCode: row[0] || '', // 매장코드
                name: row[1] || '',
                course: row[3] || '',
                order: row[4] || '',
                time: row[5] || '',
                address: row[6] || ''
            }));
        } catch (error) {
            console.error('Error fetching from Google Sheets:', error);
            return [];
        }
    }
};
