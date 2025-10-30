// get the current URL path
const currentPathURL = window.location.pathname.toString();

// function of using jsFileDownloader library to download file from web application to local/user machine
function fileDownloader(filepath, btnElement) {
  // keep the original HTML element
  const originalHTML = btnElement.html();

  // change to loading/spinner
  btnElement.html('<i class="spinner-border spinner-border-sm text-light" aria-hidden="true"></i>');

  new jsFileDownloader({ url: filepath })
    .then(function () {
      // restore to original HTML element when its done
      btnElement.html(originalHTML);
    })
    .catch(function (error) {
      // error message to console.log
      console.log(error);
      alert("Error");
      btnElement.html(originalHTML);
    });
}

$(document).ready(function () {
  const table = $("#dataTable");

  const dataTable = table.DataTable({
    ajax: currentPathURL,
    rowId: "id",
    layout: {
      topStart: null,
      topEnd: "pageLength",
      bottomStart: "info",
      bottomEnd: {
        paging: {
          firstLast: false,
          buttons: 3,
        },
      },
    },
    language: {
      lengthMenu: "Hiển thị _MENU_ dòng",
      info: "Số trang: _PAGE_ / _PAGES_",
      infoFiltered: "",
      infoEmpty: "",
      zeroRecords: "Không tìm thấy kết quả phù hợp",
      emptyTable: "Không tìm thấy thông tin dữ liệu",
      loadingRecords: "Đang tải...",
      entries: {
        _: "dòng",
        1: "dòng",
      },
      select: {
        rows: {
          0: "",
          _: "(Đã chọn %d dòng)",
        },
      },
    },
    columns: [
      { data: null, name: "selectBox", orderable: false, render: DataTable.render.select() },
      {
        data: "name",
        name: "name",
        title: "Tên / Chủ đề",
        render: function (data, type, row, meta) {
          return `<a class="text-color-accent" href="${row.uploaded_file}" target="_blank" >${data}</a>`;
        },
      },
      { data: "category", name: "category", title: "Phân loại", className: "text-center" },
      { data: "subcategory", name: "subcategory", title: "Môn học", className: "text-center" },
      { data: "file_type", name: "file_type", title: "Nhóm", className: "text-center" },
      { data: "file_language", name: "file_language", title: "Ngôn ngữ", className: "text-center" },
      { data: "last_modified", name: "last_modified", title: "Cập nhật", className: "text-center" },
      {
        data: "uploaded_file",
        name: "actions",
        title: "",
        className: "text-center",
        orderable: false,
        render: function (data, type, row, meta) {
          return `
            <button type="button" class="btn btn-sm button-color-for-downloader btn-downloader" file-url="${data}">
              <i class="bi bi-cloud-download"></i>
            </button>
          `;
        },
      },
    ],
    ordering: true,
    select: {
      style: "multi",
      items: "row",
    },
    order: [
      { name: "last_modified", dir: "desc" },
      { name: "name", dir: "asc" },
    ],
  });

  // search form (not using the default from DataTables.net)
  $("#searchInput").on("keyup", function () {
    // only search for column number 1 (name column)
    dataTable.columns([1]).search(this.value).draw();
  });

  // add class "px-0" from Bootstrap 5 to these element tags
  $("#dataTable_wrapper .d-md-flex.justify-content-between.align-items-center.col-12.dt-layout-full.col-md").addClass(
    "px-0"
  );
  $(
    "#dataTable_wrapper .d-md-flex.justify-content-between.align-items-center.dt-layout-start.col-md-auto.me-auto"
  ).addClass("px-0");
  $(
    "#dataTable_wrapper .d-md-flex.justify-content-between.align-items-center.dt-layout-end.col-md-auto.ms-auto"
  ).addClass("px-0");

  // file downloader
  $(table).on("click", ".btn-downloader", function (e) {
    e.preventDefault();

    const filepath = $(this).attr("file-url").toString();
    const btnElement = $(this);

    fileDownloader(filepath, btnElement);
  });
});
