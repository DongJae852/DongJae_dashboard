const storage = {
    KEYS: {
        BASE_DATE: 'ag_base_date',
        HOLIDAYS: 'ag_holidays',
        DELIVERY_DATA: 'ag_delivery_data', // Local inputs like box qty
        OFFICIAL_SHOPS: 'ag_official_shops', // Cached from Google Sheets
        UPLOAD_HISTORY: 'ag_upload_history'
    },

    get(key, defaultValue = null) {
        const val = localStorage.getItem(key);
        try {
            return val ? JSON.parse(val) : defaultValue;
        } catch {
            return val || defaultValue;
        }
    },

    set(key, value) {
        localStorage.setItem(key, typeof value === 'string' ? value : JSON.stringify(value));
    },

    // Specific helpers
    getHolidays() {
        return this.get(this.KEYS.HOLIDAYS, []);
    },

    setHolidays(days) {
        this.set(this.KEYS.HOLIDAYS, days);
    },

    getBaseDate() {
        return this.get(this.KEYS.BASE_DATE, '2026-01-02');
    },

    setBaseDate(date) {
        this.set(this.KEYS.BASE_DATE, date);
    },

    getInputs(date, shopCode) {
        const data = this.get(this.KEYS.DELIVERY_DATA, {});
        return data[`${date}_${shopCode}`] || {};
    },

    saveInput(date, shopCode, field, value) {
        const data = this.get(this.KEYS.DELIVERY_DATA, {});
        const key = `${date}_${shopCode}`;
        if (!data[key]) data[key] = {};
        data[key][field] = value;
        this.set(this.KEYS.DELIVERY_DATA, data);
    },

    getHiddenShops(date) {
        const hiddenKey = `ag_hidden_${date}`;
        return this.get(hiddenKey, []);
    },

    setHiddenShops(date, codes) {
        const hiddenKey = `ag_hidden_${date}`;
        this.set(hiddenKey, codes);
    },

    getCustomOrder(date, subCourse) {
        const orderKey = `ag_order_${date}_${subCourse}`;
        return this.get(orderKey, null);
    },

    setCustomOrder(date, subCourse, codes) {
        const orderKey = `ag_order_${date}_${subCourse}`;
        this.set(orderKey, codes);
    }
};
