var path = require('path'),
    fs = require('fs'),
    sys = require('util'),
    os = require('os');

var less = require('C:/Users/Jimmy/node_modules/less/lib/less');
var args = process.argv.slice(1);
var options = {
    compress: false,
    yuicompress: false,
    optimization: 1,
    silent: false,
    paths: [],
    color: true,
    strictImports: false
};

args = args.filter(function (arg) {
    var match;

    if (match = arg.match(/^-I(.+)$/)) {
        options.paths.push(match[1]);
        return false;
    }

    if (match = arg.match(/^--?([a-z][0-9a-z-]*)(?:=([^\s]+))?$/i)) { arg = match[1] }
    else { return arg }

    switch (arg) {
        case 'v':
        case 'version':
            sys.puts("lessc " + less.version.join('.') + " (LESS Compiler) [JavaScript]");
            process.exit(0);
        case 'verbose':
            options.verbose = true;
            break;
        case 's':
        case 'silent':
            options.silent = true;
            break;
        case 'strict-imports':
            options.strictImports = true;
            break;
        case 'h':
        case 'help':
            sys.puts("usage: lessc source [destination]");
            process.exit(0);
        case 'x':
        case 'compress':
            options.compress = true;
            break;
        case 'yui-compress':
            options.yuicompress = true;
            break;
        case 'no-color':
            options.color = false;
            break;
        case 'include-path':
            options.paths = match[2].split(os.type().match(/Windows/) ? ';' : ':')
                .map(function(p) {
                    if (p) {
                      return path.resolve(process.cwd(), p);
                    }
                });
            break;
        case 'O0': options.optimization = 0; break;
        case 'O1': options.optimization = 1; break;
        case 'O2': options.optimization = 2; break;
    }
});

var input = args[1];
if (input && input != '-') {
    input = path.resolve(process.cwd(), input);
}
var output = args[2];
if (output) {
    output = path.resolve(process.cwd(), output);
}

var css, fd, tree;

if (! input) {
    sys.puts("lessc: no input files");
    process.exit(1);
}

var parseLessFile = function (e, data) {
    if (e) {
        sys.puts("lessc: " + e.message);
        process.exit(1);
    }

    new(less.Parser)({
        paths: [path.dirname(input)].concat(options.paths),
        optimization: options.optimization,
        filename: input,
        strictImports: options.strictImports
    }).parse(data, function (err, tree) {
        if (err) {
            less.writeError(err, options);
            process.exit(1);
        } else {
            try {
                css = tree.toCSS({
                    compress: options.compress,
                    yuicompress: options.yuicompress
                });
                if (output) {
                    fd = fs.openSync(output, "w");
                    fs.writeSync(fd, css, 0, "utf8");
                } else {
                    sys.print(css);
                }
            } catch (e) {
                less.writeError(e, options);
                process.exit(2);
            }
        }
    });
};

if (input != '-') {
    fs.readFile(input, 'utf-8', parseLessFile);
} else {
    process.stdin.resume();
    process.stdin.setEncoding('utf8');

    var buffer = '';
    process.stdin.on('data', function(data) {
        buffer += data;
    });

    process.stdin.on('end', function() {
        parseLessFile(false, buffer);
    });
}