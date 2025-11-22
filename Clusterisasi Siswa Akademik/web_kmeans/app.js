document.addEventListener("DOMContentLoaded", () => {
  const fileUploader = document.getElementById("csvFileUploader");
  const prosesButton = document.getElementById("prosesButton");
  const hasilContainer = document.getElementById("hasil-container");
  const loadingDiv = document.getElementById("loading");

  const API_URL = "http://127.0.0.1:8002/upload_dan_klasterisasi";

  prosesButton.addEventListener("click", () => {
    const file = fileUploader.files[0];
    if (!file) {
      alert("Pilih file CSV dulu, bro!");
      return;
    }

    // Bersihkan hasil lama & tampilkan loading
    hasilContainer.innerHTML = "";
    loadingDiv.style.display = "block";
    prosesButton.disabled = true;

    // 1. Siapin FormData (BUKAN JSON)
    const formData = new FormData();
    formData.append("file_csv", file); // 'file_csv' harus SAMA kayak di API

    // 2. Kirim data ke API
    fetch(API_URL, {
      method: "POST",
      body: formData, // Kirim sebagai FormData
      // (Kita GAK PERLU 'headers', browser otomatis ngatur 'multipart/form-data')
    })
      .then((response) => response.json())
      .then((data) => {
        // Sembunyikan loading
        loadingDiv.style.display = "none";
        prosesButton.disabled = false;

        if (data.error) {
          throw new Error(data.error);
        }

        // 3. Tampilkan hasil (Looping JSON)
        console.log("Menerima data klaster:", data);

        // 'data' isinya: {"Cluster A": ["Siswa 1", "Siswa 2"], "Cluster B": ["Siswa 3"]}
        for (const namaKlaster in data) {
          // Bikin HTML buat tiap grup
          let grupHTML = `
                    <div class="cluster-grup">
                        <h3>${namaKlaster}</h3>
                        <ul>
                `;

          const daftarSiswa = data[namaKlaster];
          if (daftarSiswa.length === 0) {
            grupHTML += "<li>Tidak ada siswa di klaster ini.</li>";
          } else {
            daftarSiswa.forEach((namaSiswa) => {
              grupHTML += `<li>${namaSiswa}</li>`;
            });
          }

          grupHTML += `
                        </ul>
                    </div>
                `;

          // Tambahin ke halaman
          hasilContainer.innerHTML += grupHTML;
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        loadingDiv.style.display = "none";
        prosesButton.disabled = false;
        hasilContainer.innerHTML = `<h3 style="color: red;">Error: ${error.message}</h3>`;
      });
  });
});
