function setup(options) {
    const store = options.auxData();
    const numberInput1 = document.getElementById("minTimeAnswer");
    const numberInput2 = document.getElementById("minTimeEase");
  
    // update html when state changes
    store.subscribe((data) => {
      numberInput1.value = data["minTimeAnswer"];
      numberInput2.value = data["minTimeEase"];
    });
  
    // update config when check state changes
    numberInput1.addEventListener("change", (_) => {
      let number = 0;
      try {
        number = parseInt(numberInput1.value, 10);
      } catch (err) {}
  
      return store.update((data) => {
        return { ...data, minTimeAnswer: number };
      });

    });
    
    // update config when check state changes
    numberInput2.addEventListener("change", (_) => {
      let number = 0;
      try {
        number = parseInt(numberInput2.value, 10);
      } catch (err) {}
      
      return store.update((data) => {
        return { ...data, minTimeEase: number };
      });
    });
  }
  
  $deckOptions.then((options) => {
    options.addHtmlAddon(HTML_CONTENT, () => setup(options));
  });