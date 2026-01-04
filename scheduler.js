const scheduler = {
    COURSES: ['A', 'B', 'C', 'D', 'E'],

    isWeekend(date) {
        const day = date.getDay();
        return day === 0 || day === 6; // Sunday, Saturday
    },

    isHoliday(dateStr, holidays) {
        return holidays.includes(dateStr);
    },

    isBusinessDay(date, holidays) {
        if (this.isWeekend(date)) return false;
        const dateStr = date.toISOString().split('T')[0];
        if (this.isHoliday(dateStr, holidays)) return false;
        return true;
    },

    getBusinessDaysBetween(start, end, holidays) {
        let count = 0;
        let current = new Date(start);

        // We need to handle the direction
        const step = start <= end ? 1 : -1;

        while (current.toISOString().split('T')[0] !== end.toISOString().split('T')[0]) {
            if (this.isBusinessDay(current, holidays)) {
                count += step;
            }
            current.setDate(current.getDate() + step);
        }
        return count;
    },

    // Important: Calculate shift-aware course
    // If a day is a holiday, we skip calculating for it and the rotation "pauses"
    getCourseForDate(targetDateStr, baseDateStr, holidays) {
        const targetDate = new Date(targetDateStr);
        const baseDate = new Date(baseDateStr);

        if (!this.isBusinessDay(targetDate, holidays)) {
            return null; // No delivery on holidays/weekends
        }

        // Calculation logic:
        // We start from baseDate (which is 'B').
        // We count business days between baseDate and targetDate.
        // The business day count determines the rotation index.

        const diff = this.getBusinessDaysBetween(baseDate, targetDate, holidays);

        // Base is 'B', which is index 1
        const startIndex = 1;
        const totalCourses = this.COURSES.length;

        // Use modulo to wrap around A-E
        let courseIndex = (startIndex + diff) % totalCourses;
        if (courseIndex < 0) courseIndex += totalCourses;

        const courseLetter = this.COURSES[courseIndex];

        // Return a simulated sub-course for now (e.g. B1, B2...)
        // In real data, we usually match by the letter.
        return courseLetter;
    }
};
