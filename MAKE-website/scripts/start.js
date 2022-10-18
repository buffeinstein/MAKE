async function start() {
    if (state.college_id !== null) {
        displayLoggedIn();
        await updateUserInfo();
    } else {
        displayLoggedOut();
    }

    //animateChangeFonts();

    renderQuizInfo();
    renderCheckouts();
    renderEquipment();
    
    // Url param, get page
    const url_params = new URLSearchParams(window.location.search);
    const page = url_params.get("p");
    if (page !== null) {
        setPage(page);
    }
    
    setInterval(fetchInventory, 100000);
    setInterval(fetchStudentStorage, 10000);
    setInterval(fetchSchedule, 100000);
    //setInterval(fetchPrinters, 10000);

    fetchInventory().then(() => {
        submitSearch();
        document.getElementById("inventory-search-input").addEventListener("keyup", submitSearch);
        document.getElementById("inventory-in-stock").addEventListener("change", submitSearch);
        document.getElementById("room-select").addEventListener("change", submitSearch);
        document.getElementById("tool-material-select").addEventListener("change", submitSearch);
    });
    fetchStudentStorage();
    fetchSchedule();
    //fetchPrinters();
}

start();