// Daily Streak Tracking System
class StreakTracker {
    constructor() {
        this.storageKey = 'userStreak';
        this.init();
    }

    init() {
        const streakData = this.getStreakData();
        this.updateStreak(streakData);
    }

    getStreakData() {
        const stored = localStorage.getItem(this.storageKey);
        if (stored) {
            return JSON.parse(stored);
        }
        
        // Initialize new streak data
        const newStreakData = {
            currentStreak: 0,
            longestStreak: 0,
            lastLoginDate: null,
            totalDays: 0
        };
        
        this.saveStreakData(newStreakData);
        return newStreakData;
    }

    saveStreakData(data) {
        localStorage.setItem(this.storageKey, JSON.stringify(data));
    }

    getTodayDateString() {
        return new Date().toDateString();
    }

    getYesterdayDateString() {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        return yesterday.toDateString();
    }

    updateStreak(streakData) {
        const today = this.getTodayDateString();
        const yesterday = this.getYesterdayDateString();
        
        if (!streakData.lastLoginDate) {
            // First time login
            streakData.currentStreak = 1;
            streakData.longestStreak = 1;
            streakData.lastLoginDate = today;
            streakData.totalDays = 1;
        } else if (streakData.lastLoginDate === today) {
            // Already logged in today, no change
            return streakData;
        } else if (streakData.lastLoginDate === yesterday) {
            // Consecutive day login
            streakData.currentStreak += 1;
            streakData.longestStreak = Math.max(streakData.longestStreak, streakData.currentStreak);
            streakData.lastLoginDate = today;
            streakData.totalDays += 1;
        } else {
            // Streak broken
            streakData.currentStreak = 1;
            streakData.lastLoginDate = today;
            streakData.totalDays += 1;
        }
        
        this.saveStreakData(streakData);
        return streakData;
    }

    getCurrentStreak() {
        const streakData = this.getStreakData();
        return this.updateStreak(streakData);
    }

    resetStreak() {
        const resetData = {
            currentStreak: 0,
            longestStreak: 0,
            lastLoginDate: null,
            totalDays: 0
        };
        this.saveStreakData(resetData);
        return resetData;
    }
}

// Global streak tracker instance
window.streakTracker = new StreakTracker();