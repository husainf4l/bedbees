/**
 * BedBees Calendar Management System
 * Handles interactive calendar for availability and pricing management
 */

class BedBeesCalendar {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.listingId = options.listingId;
        this.listingType = options.listingType || 'accommodation'; // 'accommodation' or 'tour'
        this.currentDate = new Date();
        this.selectedDates = [];
        this.calendarData = {};
        
        this.init();
    }
    
    init() {
        this.loadCalendarData();
        this.setupEventListeners();
    }
    
    async loadCalendarData() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        // Get first and last day of the month
        const startDate = new Date(year, month, 1);
        const endDate = new Date(year, month + 1, 0);
        
        const startDateStr = this.formatDate(startDate);
        const endDateStr = this.formatDate(endDate);
        
        try {
            const endpoint = this.listingType === 'accommodation' 
                ? `/api/accommodation/${this.listingId}/calendar/`
                : `/api/tour/${this.listingId}/calendar/`;
            
            const response = await fetch(`${endpoint}?start_date=${startDateStr}&end_date=${endDateStr}`);
            const data = await response.json();
            
            if (data.success) {
                this.calendarData = {};
                data.calendar.forEach(day => {
                    this.calendarData[day.date] = day;
                });
                this.renderCalendar();
                this.updateStats(data.stats);
            }
        } catch (error) {
            console.error('Error loading calendar:', error);
            this.showError('Failed to load calendar data');
        }
    }
    
    renderCalendar() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        // Update month/year display
        const monthNames = ["January", "February", "March", "April", "May", "June",
                           "July", "August", "September", "October", "November", "December"];
        document.getElementById('calendar-month-year').textContent = `${monthNames[month]} ${year}`;
        
        // Get calendar grid
        const grid = document.getElementById('calendar-grid');
        grid.innerHTML = '';
        
        // Calculate calendar days
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const today = new Date();
        
        // Add empty cells for days before month starts
        for (let i = 0; i < firstDay; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.className = 'calendar-day-empty';
            grid.appendChild(emptyCell);
        }
        
        // Add days of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            const dateStr = this.formatDate(date);
            const dayData = this.calendarData[dateStr] || {};
            
            const dayCell = this.createDayCell(day, date, dayData);
            grid.appendChild(dayCell);
        }
    }
    
    createDayCell(day, date, dayData) {
        const cell = document.createElement('div');
        const isToday = this.isToday(date);
        const isPast = date < new Date().setHours(0, 0, 0, 0);
        
        // Base classes
        cell.className = 'calendar-day p-3 border rounded-lg cursor-pointer hover:shadow-md transition-all';
        
        // Status-based styling
        if (isPast) {
            cell.className += ' bg-gray-100 text-gray-400 cursor-not-allowed';
        } else if (dayData.is_blocked) {
            cell.className += ' bg-red-50 border-red-300';
        } else if (dayData.is_fully_booked) {
            cell.className += ' bg-blue-50 border-blue-300';
        } else if (dayData.is_available) {
            cell.className += ' bg-green-50 border-green-200';
        } else {
            cell.className += ' bg-gray-100 border-gray-300';
        }
        
        if (isToday) {
            cell.className += ' border-2 border-blue-500';
        }
        
        // Day number
        const dayNumber = document.createElement('div');
        dayNumber.className = 'font-bold text-sm mb-1';
        dayNumber.textContent = day;
        cell.appendChild(dayNumber);
        
        // Price display
        if (dayData.price && !isPast) {
            const price = document.createElement('div');
            price.className = 'text-xs font-semibold';
            
            if (dayData.is_blocked) {
                price.className += ' text-red-700';
                price.textContent = '✕ Blocked';
            } else if (dayData.is_fully_booked) {
                price.className += ' text-blue-700';
                price.textContent = '✓ Booked';
            } else if (dayData.is_available) {
                price.className += ' text-green-700';
                price.textContent = `$${dayData.price}`;
            } else {
                price.className += ' text-gray-500';
                price.textContent = 'Closed';
            }
            
            cell.appendChild(price);
        }
        
        // Availability indicator for accommodations
        if (this.listingType === 'accommodation' && dayData.rooms_available !== undefined && !isPast) {
            const rooms = document.createElement('div');
            rooms.className = 'text-xs text-gray-600 mt-1';
            rooms.textContent = `${dayData.rooms_available} left`;
            cell.appendChild(rooms);
        }
        
        // Availability indicator for tours
        if (this.listingType === 'tour' && dayData.spots_available !== undefined && !isPast) {
            const spots = document.createElement('div');
            spots.className = 'text-xs text-gray-600 mt-1';
            spots.textContent = `${dayData.spots_available} spots`;
            cell.appendChild(spots);
        }
        
        // Click handler (only for future dates)
        if (!isPast) {
            cell.addEventListener('click', () => this.openEditModal(date, dayData));
        }
        
        return cell;
    }
    
    openEditModal(date, dayData) {
        const modal = document.getElementById('edit-date-modal');
        const dateDisplay = document.getElementById('modal-date-display');
        
        // Format date for display
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateDisplay.textContent = date.toLocaleDateString('en-US', options);
        
        // Store current date for saving
        modal.dataset.editDate = this.formatDate(date);
        
        // Populate form fields
        document.getElementById('date-open').checked = !dayData.is_blocked;
        document.getElementById('day-available').checked = dayData.is_available !== false;
        document.getElementById('day-price').value = dayData.price || 0;
        document.getElementById('day-min-stay').value = dayData.minimum_stay || 1;
        
        if (this.listingType === 'accommodation') {
            document.getElementById('day-total-rooms').value = dayData.total_rooms || 1;
            document.getElementById('day-rooms-blocked').value = dayData.rooms_blocked || 0;
        }
        
        // Show modal
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
    
    closeEditModal() {
        const modal = document.getElementById('edit-date-modal');
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
    
    async saveDate() {
        const modal = document.getElementById('edit-date-modal');
        const dateStr = modal.dataset.editDate;
        
        const updateData = {
            date: dateStr,
            is_available: document.getElementById('day-available').checked,
            is_blocked: !document.getElementById('date-open').checked,
            price: parseFloat(document.getElementById('day-price').value),
            minimum_stay: parseInt(document.getElementById('day-min-stay').value),
        };
        
        if (this.listingType === 'accommodation') {
            updateData.total_rooms = parseInt(document.getElementById('day-total-rooms').value);
            updateData.rooms_blocked = parseInt(document.getElementById('day-rooms-blocked').value);
        }
        
        try {
            const endpoint = `/api/accommodation/${this.listingId}/calendar/update/`;
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updateData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showSuccess('Date updated successfully');
                this.closeEditModal();
                this.loadCalendarData();
            } else {
                this.showError(data.error || 'Failed to update date');
            }
        } catch (error) {
            console.error('Error saving date:', error);
            this.showError('Failed to save changes');
        }
    }
    
    async bulkEdit(startDate, endDate, updates) {
        const startDateStr = this.formatDate(startDate);
        const endDateStr = this.formatDate(endDate);
        
        const bulkData = {
            start_date: startDateStr,
            end_date: endDateStr,
            ...updates
        };
        
        try {
            const endpoint = `/api/accommodation/${this.listingId}/calendar/bulk-update/`;
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bulkData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showSuccess(`Updated ${data.dates_updated} dates`);
                this.loadCalendarData();
            } else {
                this.showError(data.error || 'Bulk update failed');
            }
        } catch (error) {
            console.error('Error in bulk update:', error);
            this.showError('Bulk update failed');
        }
    }
    
    previousMonth() {
        this.currentDate.setMonth(this.currentDate.getMonth() - 1);
        this.loadCalendarData();
    }
    
    nextMonth() {
        this.currentDate.setMonth(this.currentDate.getMonth() + 1);
        this.loadCalendarData();
    }
    
    goToToday() {
        this.currentDate = new Date();
        this.loadCalendarData();
    }
    
    formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
    
    isToday(date) {
        const today = new Date();
        return date.getDate() === today.getDate() &&
               date.getMonth() === today.getMonth() &&
               date.getFullYear() === today.getFullYear();
    }
    
    updateStats(stats) {
        // Update statistics in the UI if elements exist
        if (document.getElementById('stat-available-days')) {
            document.getElementById('stat-available-days').textContent = stats.available_days;
        }
        if (document.getElementById('stat-booked-days')) {
            document.getElementById('stat-booked-days').textContent = stats.booked_days;
        }
        if (document.getElementById('stat-avg-price')) {
            document.getElementById('stat-avg-price').textContent = `$${stats.avg_price.toFixed(0)}`;
        }
        if (document.getElementById('stat-occupancy')) {
            document.getElementById('stat-occupancy').textContent = `${stats.avg_occupancy.toFixed(0)}%`;
        }
    }
    
    setupEventListeners() {
        // Month navigation
        document.getElementById('prev-month')?.addEventListener('click', () => this.previousMonth());
        document.getElementById('next-month')?.addEventListener('click', () => this.nextMonth());
        document.getElementById('goToToday')?.addEventListener('click', () => this.goToToday());
        
        // Modal close
        document.querySelectorAll('[onclick="closeEditModal()"]').forEach(btn => {
            btn.addEventListener('click', () => this.closeEditModal());
        });
        
        // Save button
        document.getElementById('save-date-btn')?.addEventListener('click', () => this.saveDate());
    }
    
    showSuccess(message) {
        // Simple success notification (you can enhance this)
        alert(message);
    }
    
    showError(message) {
        // Simple error notification (you can enhance this)
        alert('Error: ' + message);
    }
}

// Global functions for backwards compatibility
function previousMonth() {
    if (window.bedBeesCalendar) {
        window.bedBeesCalendar.previousMonth();
    }
}

function nextMonth() {
    if (window.bedBeesCalendar) {
        window.bedBeesCalendar.nextMonth();
    }
}

function goToToday() {
    if (window.bedBeesCalendar) {
        window.bedBeesCalendar.goToToday();
    }
}

function closeEditModal() {
    if (window.bedBeesCalendar) {
        window.bedBeesCalendar.closeEditModal();
    }
}

function saveDate() {
    if (window.bedBeesCalendar) {
        window.bedBeesCalendar.saveDate();
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BedBeesCalendar;
}
