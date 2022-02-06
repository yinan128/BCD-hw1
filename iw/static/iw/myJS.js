function placeLayer(id) {
    let clicked = document.getElementById("facility"+id)
    clicked.setAttribute("onclick", "removeLayer(" + id + ")")
    clicked.setAttribute("class", "btn btn-primary")
    let parent = document.getElementsByClassName("plan_layers").item(0)
    parent.innerHTML += '<img src="/planImage/' + id + '" alt="nothing" id="facilityImage' + id + '"' + ' style="z-index:' + id + '">'
}

function removeLayer(id) {
    let clicked = document.getElementById("facility"+id)
    clicked.setAttribute("onclick", "placeLayer(" + id + ")")
    clicked.setAttribute("class", "btn btn-outline-primary")
    let parent = document.getElementsByClassName("plan_layers").item(0)
    parent.removeChild(document.getElementById("facilityImage" + id))
}


function updateError() {
}

function seeMoreOn(id) {
    let target_modal = document.getElementById("modal_" + id)
    if (target_modal == null) {
        $.ajax({
            url: "/getSpecification/" + id,
            dataType : "json",
            success: updateModals,
            error: updateError
        })
    } else {
        showModal(id)
    }
}


function showModal(id) {
    let myModal = new bootstrap.Modal(document.getElementById('modal_' + id), {
        keyboard: false
    })
    myModal.show()
}


function updateModals(response) {
    $(response).each(function() {
        $("#modals")[0].innerHTML += modalFormatter(this);
        showModal(this.id)
    })
}

function modalFormatter(response) {
    var replacements_placeholder =
        {
            "%ID%":response.id,
            "%MANU%":response.manufacturer,
            "%DATE%": response.dateInstalled,
            "%COUNT%": response.count,
            "%DESCRIPTION%": response.description,
        }


    var placeholder =
        '<div class="modal fade" id="modal_%ID%" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\n' +
        '  <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg">\n' +
        '    <div class="modal-content">\n' +
        '      <div class="modal-header">\n' +
        '        <h5 class="modal-title" id="exampleModalLabel">More Information</h5>\n' +
        '        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\n' +
        '      </div>\n' +
        '      <div class="modal-body">\n' +
        '          <div class="container">\n' +
        '              <!-- row 1 table-->\n' +
        '              <div class="row">\n' +
        '              <div class="col"></div>\n' +
        '              <div class="col-11">\n' +
        '                  <h5>Specifications</h5>\n' +
        '                  <table class="table caption-top">\n' +
        '                    <tbody>\n' +
        '                        <tr>\n' +
        '                          <th scope="row">manufacturer</th>\n' +
        '                          <td>%MANU%</td>\n' +
        '                        </tr>\n' +
        '                        <tr>\n' +
        '                          <th scope="row">date</th>\n' +
        '                          <td>%DATE%</td>\n' +
        '                        </tr>\n' +
        '                        <tr>\n' +
        '                          <th scope="row">count</th>\n' +
        '                          <td>%COUNT%</td>\n' +
        '                        </tr>\n' +
        '                    </tbody>\n' +
        '                  </table>\n' +
        '                  <br>\n' +
        '              </div>\n' +
        '              <div class="col"></div>\n' +
        '              </div>\n' +
        '              <!-- row 2 long text-->\n' +
        '              <div class="row">\n' +
        '                  <div class="col"></div>\n' +
        '                  <div class="col-11">\n' +
        '                      <h5>Description</h5>\n' +
        '                        %DESCRIPTION%\n' +
        '                      <br>\n' +
        '                      <br>\n' +
        '                  </div>\n' +
        '                  <div class="col"></div>\n' +
        '              </div>\n' +
        '              <!-- row 3 pictures-->\n' +
        '              <div class="row">\n' +
        '                  <div class="col"></div>\n' +
        '                  <div class="col-11">\n' +
        '                      <h5>Pictures</h5>\n' +
        '                  </div>\n' +
        '                  <div class="col"></div>\n' +
        '              </div>\n' +
        '              <!-- row 3.5 pictures-->\n' +
                            pictureFormatter(response.pictureIds) +
        '          </div>\n' +
        '      </div>\n' +
        '      <div class="modal-footer">\n' +
        '        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>\n' +
        '      </div>\n' +
        '    </div>\n' +
        '  </div>\n' +
        '</div>'

    placeholder = placeholder.replace(/%\w+%/g, function(all) {
       return replacements_placeholder[all] || all;
    });

    return placeholder
}

function pictureFormatter(ids) {
    let result = ""
    for (let i=0; i< ids.length; i++) {
        let id = ids[i]
        result +=
            '<div class="row">\n' +
            ' <div class="col"></div>\n' +
            ' <img src="' + picture_url + id + '" class="col-11" alt="...">\n' +
            ' <div class="col"></div>\n' +
            '</div>\n'
    }
    return result
}


function acquireHistoric(id) {
    let target_modal = document.getElementById("historicModal_" + id)
    if (target_modal == null) {
        $.ajax({
            url: "/get-historic/" + id,
            dataType : "json",
            success: updateHistoricModals,
            error: updateError
        })
    } else {
        showHistoricModal(id)
    }
}

function showHistoricModal(id) {
    let myModal = new bootstrap.Modal(document.getElementById('historicModal_' + id), {
        keyboard: false
    })
    myModal.show()
}

function updateHistoricModals(response) {
    $("#modals")[0].innerHTML += historicModalFormatter(response);
    document.getElementById("scriptForHistoric_" + response.id).innerHTML += historicScriptFormatter(response)
    showHistoricModal(response.id)
}

function historicScriptFormatter(response) {
    let ts = []
    for (let i = 0; i < response.timestamps.length; i++) {
        ts.push("'" + response.timestamps[i] + "'")
    }

    let replacements =
        {
            "%ts%":ts,
            "%vals%":response.values,
            "%ID%":response.id,
        }

    let placeholder =
        '        let trace_%ID% = {\n' +
        '            x: [%ts%],\n' +
        '            y: [%vals%],\n' +
        '            type: \'scatter\'\n' +
        '        };\n' +
        '        let data_%ID% = [trace_%ID%];\n' +
        '        let layout_%ID% = {\n' +
        '            title: "nothing"\n' +
        '        };\n' +
        '        Plotly.newPlot(\'historicChart_%ID%\', data_%ID%, layout_%ID%);\n'

    placeholder = placeholder.replace(/%\w+%/g, function(all) {
       return replacements[all] || all;
    });

    return placeholder
}

function historicModalFormatter(response) {
    let replacements =
        {
            "%ID%":response.id,
        }

    let placeholder =
        '<div class="modal fade" id="historicModal_%ID%" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\n' +
        '  <div class="modal-dialog modal-fullscreen">\n' +
        '    <div class="modal-content">\n' +
        '      <div class="modal-header">\n' +
        '        <h5 class="modal-title" id="exampleModalLabel">Historic Data</h5>\n' +
        '        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\n' +
        '      </div>\n' +
        '      <div class="modal-body">\n' +
        '          <div class="container" id="historicChart_%ID%">\n' +
        '          </div>\n' +
        '      </div>\n' +
        '      <div class="modal-footer">\n' +
        '        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>\n' +
        '      </div>\n' +
        '    </div>\n' +
        '  </div>\n' +
        '</div>'

    placeholder = placeholder.replace(/%\w+%/g, function(all) {
       return replacements[all] || all;
    });

    return placeholder
}
