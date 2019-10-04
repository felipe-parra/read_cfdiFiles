 #!/usr/bin/env node

// import FileSystem, to use commands
const fs = require("fs");
const xml2js = require("xml2js");
const parser = new xml2js.Parser({ attrkey: "ATTR" });

/* // read file xml
fs.readFile(
  "sample.xml",
  //callback function that is called when reading file is done
  (err, data) => {
    if (err) throw err;
    // data is buffering containing file content
    console.log(data.toString("utf8"));
  }
); */

// this example reads the file synchronously
// you can read it asynchronously also
let xml_string = fs.readFileSync("sample.xml", "utf8");

class Factura {
  constructor(folio, fecha, importe, uuid, tipo, fechaTimbrado) {
    this.folio = folio;
    this.fecha = fecha;
    this.importe = importe;
    this.uuid = uuid;
    this.tipo = tipo;
    this.fechaTimbrado = fechaTimbrado;
  }
}

class Emisor {
  constructor(rfc, nombre) {
    this.rfc = rfc;
    this.nombre = nombre;
    this.tipo = "Emisor";
  }
}

class Receptor {
  constructor(rfc, nombre) {
    this.rfc = rfc;
    this.nombre = nombre;
    this.tipo = "Receptor";
  }
}

const COMPROBANTE = "cfdi:Comprobante";
const TFD = "tfd:TimbreFiscalDigital";
const ATTR = "ATTR";

const factura = new Factura();
const emisor = new Emisor();
const receptor = new Receptor();

let xmlResult;

const extractEmpresa = (empresa, tipo, xmlResult) => {
  if (tipo === "Emisor" || tipo === "Receptor") {
    const extract = xmlResult[COMPROBANTE]["cfdi:" + tipo];
    extract.forEach(data => {
      if (data[ATTR]["Rfc"]) {
        empresa.rfc = data[ATTR]["Rfc"];
      }
      if (data[ATTR]["Nombre"]) {
        empresa.nombre = data[ATTR]["Nombre"];
      }
    });
  }
  return empresa;
};

const extractComplemento = (complemento, xmlResult) => {
  const extract = xmlResult[COMPROBANTE]["cfdi:Complemento"];
  let dataComplemento;
  extract.map((e, i) => {
    const data = e[TFD];
    data.forEach(e => {
      dataComplemento = e[ATTR][complemento];
    });
  });
  return dataComplemento;
};

const createFactura = (factura, xmlResult) => {
  const extract = xmlResult[COMPROBANTE][ATTR];
  factura.folio = extract["Serie"] + extract["Folio"];
  factura.importe = extract["Total"];
  factura.fecha = extract["Fecha"];
  factura.tipo = extract["TipoDeComprobante"];
  factura.uuid = extractComplemento("UUID", xmlResult);
  factura.fechaTimbrado = extractComplemento("FechaTimbrado", xmlResult);
};

parser.parseString(xml_string, (error, result) => {
  if (error === null) {
    xmlResult = result;
  } else {
    console.log(error);
  }
});

const creationFunc = () => {
  createFactura(factura, xmlResult);
  extractEmpresa(emisor, "Emisor", xmlResult);
  extractEmpresa(receptor, "Receptor", xmlResult);
};

creationFunc();
console.log(factura);
console.log(emisor);
console.log(receptor);
