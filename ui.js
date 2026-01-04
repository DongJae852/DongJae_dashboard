const ui = {
    state: {
        currentDate: new Date().toISOString().split('T')[0],
        shops: [],
        loading: true,
        showHidden: false
    },

    async init() {
        const today = new Date().toISOString().split('T')[0];
        this.handleDateChange(today);
        this.renderHolidays();
        document.getElementById('base-date').value = storage.getBaseDate();

        // Fetch real data
        console.log('Fetching shops from Google Sheets...');
        this.state.shops = await api.fetchShops();
        this.state.loading = false;

        this.render();
        lucide.createIcons();
    },

    cleanShopName(name) {
        if (!name) return '';
        if (name.includes('직영점')) return name;
        // Remove (판매점), (가맹점) and symbols like (◇), ◇, (◆), ◆, (□), □, (■), ■ etc.
        return name.replace(/\(판매점\)|\(가맹점\)|\([\u25A0-\u25FF\u2600-\u26FF]\)|[\u25A0-\u25FF\u2600-\u26FF]/g, '').trim();
    },

    render() {
        const containerEl = document.getElementById('tables-container');
        const noDataEl = document.getElementById('no-data');
        const badgeEl = document.getElementById('current-course-badge');

        if (!containerEl) return;
        containerEl.innerHTML = '';

        if (this.state.loading) {
            containerEl.innerHTML = `
                <div class="bg-white rounded-2xl p-20 text-center text-slate-400 border border-slate-200">
                    <div class="flex flex-col items-center gap-2">
                        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                        구글 시트 데이터를 불러오는 중...
                    </div>
                </div>`;
            return;
        }

        const holidays = storage.getHolidays();
        const baseDate = storage.getBaseDate();
        const courseLetter = scheduler.getCourseForDate(this.state.currentDate, baseDate, holidays);

        if (!courseLetter) {
            noDataEl.classList.remove('hidden');
            badgeEl.textContent = '배송 없음 (휴일/주말)';
            badgeEl.className = 'px-3 py-1 bg-slate-100 text-slate-500 rounded-full text-sm font-semibold';
            return;
        }

        noDataEl.classList.add('hidden');
        badgeEl.textContent = `${courseLetter} 코스 배송일`;
        badgeEl.className = 'px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-semibold';

        const hiddenCodes = storage.getHiddenShops(this.state.currentDate);

        // Filter shops by course letter
        const activeShops = this.state.shops.filter(s => s.course && s.course.startsWith(courseLetter));

        if (activeShops.length === 0) {
            containerEl.innerHTML = `
                <div class="bg-white rounded-2xl p-20 text-center text-slate-400 border border-slate-200">
                    해당 코스에 할당된 매장이 없습니다.
                </div>`;
            return;
        }

        // Group by sub-course (e.g., B1, B2)
        const groups = {};
        activeShops.forEach(shop => {
            if (!groups[shop.course]) groups[shop.course] = [];
            groups[shop.course].push(shop);
        });

        const sortedSubCourses = Object.keys(groups).sort();

        sortedSubCourses.forEach(subCourse => {
            let shopsInGroup = groups[subCourse];
            const customOrder = storage.getCustomOrder(this.state.currentDate, subCourse);

            // Apply custom order if exists
            if (customOrder) {
                const shopMap = new Map(shopsInGroup.map(s => [s.code, s]));
                shopsInGroup = customOrder
                    .map(code => shopMap.get(code))
                    .filter(Boolean);

                // Append any new shops that were not in custom order
                const missing = activeShops.filter(s => s.course === subCourse && !customOrder.includes(s.code));
                shopsInGroup = [...shopsInGroup, ...missing];
            } else {
                shopsInGroup.sort((a, b) => parseInt(a.order) - parseInt(b.order));
            }

            const groupSection = document.createElement('div');
            groupSection.className = 'space-y-4 mb-10';

            // Filter out hidden ones if not showing them
            const renderShops = this.state.showHidden ? shopsInGroup : shopsInGroup.filter(s => !hiddenCodes.includes(s.code));
            let serialCount = 1;

            groupSection.innerHTML = `
                <div class="flex items-center justify-between px-2">
                    <div class="flex items-center gap-3">
                        <div class="w-1.5 h-6 bg-indigo-600 rounded-full"></div>
                        <h3 class="text-xl font-bold text-slate-800">${subCourse} 코스</h3>
                        <span class="text-sm text-slate-400 font-medium">${renderShops.length}개 대상</span>
                    </div>
                    <button onclick="ui.toggleShowHidden()" class="flex items-center gap-2 text-xs font-semibold ${this.state.showHidden ? 'text-indigo-600' : 'text-slate-400'} hover:text-indigo-700">
                        <i data-lucide="${this.state.showHidden ? 'eye' : 'eye-off'}" class="w-4 h-4"></i>
                        ${this.state.showHidden ? '숨긴 매장 감추기' : '숨긴 매장 보기'}
                    </button>
                </div>
                <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse min-w-max">
                            <thead>
                                <tr class="bg-slate-50 border-b border-slate-200 whitespace-nowrap">
                                    <th class="px-2 py-3 w-8"></th>
                                    <th class="px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider w-16 text-center">순번</th>
                                    <th class="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">매장명</th>
                                    <th class="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">납품코드</th>
                                    <th class="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider text-center">영업시간</th>
                                    <th class="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">주소</th>
                                    <th class="px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider w-24 text-center">박스수량</th>
                                    <th class="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider min-w-[150px] text-center">전달품목</th>
                                    <th class="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider text-center">본사수거</th>
                                    <th class="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider text-center">체크사항</th>
                                    <th class="px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider w-24 text-center">출고수량</th>
                                    <th class="px-4 py-3 w-10"></th>
                                </tr>
                            </thead>
                            <tbody id="tbody-${subCourse}" class="divide-y divide-slate-100">
                                ${renderShops.map((shop, idx) => {
                const isHidden = hiddenCodes.includes(shop.code);
                const inputs = storage.getInputs(this.state.currentDate, shop.code);
                const cleanedName = this.cleanShopName(shop.name);
                const serial = isHidden ? '-' : serialCount++;

                return `
                                        <tr data-code="${shop.code}" class="hover:bg-slate-50 transition-all ${isHidden ? 'shop-hidden' : ''}">
                                            <td class="px-2 py-4 text-center">
                                                <div class="drag-handle">
                                                    <i data-lucide="grip-vertical" class="w-4 h-4"></i>
                                                </div>
                                            </td>
                                            <td class="px-4 py-4 text-center text-sm text-slate-400 font-medium">${serial}</td>
                                            <td class="px-6 py-4 font-bold text-slate-800">${cleanedName}</td>
                                            <td class="px-6 py-4 text-sm text-slate-500 font-mono">${shop.code}</td>
                                            <td class="px-6 py-4 text-sm text-indigo-600 font-semibold text-center">${shop.time}</td>
                                            <td class="px-6 py-4 text-sm text-slate-500">${shop.address}</td>
                                            <td class="px-4 py-4">
                                                <input type="text" value="${inputs.boxQty || ''}" onblur="ui.save('${shop.code}', 'boxQty', this.value)" class="editable w-full px-2 py-1 rounded text-sm bg-transparent border-b border-transparent hover:border-slate-200 text-center" tabindex="${1000 + idx * 5 + 1}">
                                            </td>
                                            <td class="px-6 py-4">
                                                <input type="text" value="${inputs.deliveryItems || ''}" onblur="ui.save('${shop.code}', 'deliveryItems', this.value)" class="editable w-full px-2 py-1 rounded text-sm bg-transparent border-b border-transparent hover:border-slate-200" tabindex="${1000 + idx * 5 + 2}">
                                            </td>
                                            <td class="px-6 py-4">
                                                <input type="text" value="${inputs.hqCollect || ''}" onblur="ui.save('${shop.code}', 'hqCollect', this.value)" class="editable w-full px-2 py-1 rounded text-sm bg-transparent border-b border-transparent hover:border-slate-200" tabindex="${1000 + idx * 5 + 3}">
                                            </td>
                                            <td class="px-6 py-4">
                                                <input type="text" value="${inputs.checkNotes || ''}" onblur="ui.save('${shop.code}', 'checkNotes', this.value)" class="editable w-full px-2 py-1 rounded text-sm bg-transparent border-b border-transparent hover:border-slate-200" tabindex="${1000 + idx * 5 + 4}">
                                            </td>
                                            <td class="px-4 py-4">
                                                <input type="text" value="${inputs.outQty || ''}" onblur="ui.save('${shop.code}', 'outQty', this.value)" class="editable w-full px-2 py-1 rounded text-sm bg-transparent border-b border-transparent hover:border-slate-200 text-center" tabindex="${1000 + idx * 5 + 5}">
                                            </td>
                                            <td class="px-4 py-4 text-center">
                                                <button onclick="ui.toggleHide('${shop.code}')" class="text-slate-300 hover:text-indigo-600 transition-colors" title="${isHidden ? '숨기기 해제' : '매장 숨기기'}">
                                                    <i data-lucide="${isHidden ? 'eye-off' : 'eye'}" class="w-4 h-4"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    `;
            }).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
            containerEl.appendChild(groupSection);

            // Initialize Sortable
            const tbody = document.getElementById(`tbody-${subCourse}`);
            new Sortable(tbody, {
                handle: '.drag-handle',
                animation: 150,
                ghostClass: 'sortable-ghost',
                onEnd: (evt) => {
                    const codes = Array.from(tbody.querySelectorAll('tr')).map(tr => tr.dataset.code);
                    storage.setCustomOrder(this.state.currentDate, subCourse, codes);
                    this.render(); // Re-render for serial numbers
                }
            });
        });
        lucide.createIcons();
    },

    toggleHide(code) {
        let hidden = storage.getHiddenShops(this.state.currentDate);
        if (hidden.includes(code)) {
            hidden = hidden.filter(c => c !== code);
        } else {
            hidden.push(code);
        }
        storage.setHiddenShops(this.state.currentDate, hidden);
        this.render();
    },

    toggleShowHidden() {
        this.state.showHidden = !this.state.showHidden;
        this.render();
    },

    save(shopCode, field, value) {
        storage.saveInput(this.state.currentDate, shopCode, field, value);
    },

    handleDateChange(val) {
        this.state.currentDate = val;
        document.getElementById('target-date').value = val;
        this.render();
    },

    prevDay() {
        const d = new Date(this.state.currentDate);
        d.setDate(d.getDate() - 1);
        this.handleDateChange(d.toISOString().split('T')[0]);
    },

    nextDay() {
        const d = new Date(this.state.currentDate);
        d.setDate(d.getDate() + 1);
        this.handleDateChange(d.toISOString().split('T')[0]);
    },

    setToday() {
        this.handleDateChange(new Date().toISOString().split('T')[0]);
    },

    showSettings() {
        document.getElementById('settings-modal').classList.remove('hidden');
    },

    hideSettings() {
        const baseDate = document.getElementById('base-date').value;
        storage.setBaseDate(baseDate);
        document.getElementById('settings-modal').classList.add('hidden');
        this.render();
    },

    addHoliday() {
        const dateInput = document.getElementById('new-holiday');
        const date = dateInput.value;
        if (!date) return;

        const holidays = storage.getHolidays();
        if (!holidays.includes(date)) {
            holidays.push(date);
            storage.setHolidays(holidays);
            this.renderHolidays();
            this.render();
        }
        dateInput.value = '';
    },

    removeHoliday(date) {
        let holidays = storage.getHolidays();
        holidays = holidays.filter(h => h !== date);
        storage.setHolidays(holidays);
        this.renderHolidays();
        this.render();
    },

    renderHolidays() {
        const container = document.getElementById('holiday-list');
        const holidays = storage.getHolidays();
        if (!container) return;
        container.innerHTML = holidays.map(h => `
            <div class="flex items-center gap-1 bg-slate-100 px-3 py-1 rounded-full text-xs font-semibold text-slate-600">
                ${h}
                <button onclick="ui.removeHoliday('${h}')" class="text-slate-400 hover:text-red-500">
                    <i data-lucide="x" class="w-3 h-3"></i>
                </button>
            </div>
        `).join('');
        lucide.createIcons();
    }
};

// Start
ui.init();
