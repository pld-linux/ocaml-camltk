%define		ver	418
Summary:	Tk binding for OCaml
Summary(pl):	Wi±zania Tk dla OCamla
Name:		ocaml-camltk
Version:	0.%{ver}
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.inria.fr/INRIA/Projects/cristal/caml-light/bazar-ocaml/ocamltk/ocamltk%{ver}.tar.gz
# Source0-md5:	9cb2c457b6425dd63fb53b93fd074e2e
Patch0:		%{name}-ac.patch
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	autoconf
BuildRequires:	automake
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library for interfacing Objective Caml with the scripting language
Tcl/Tk.

This package contains files needed to run bytecode executables using
this library.

%description -l pl
Biblioteka pozwalaj±ca na ³±czenie programów napisanych w OCamlu i
Tcl/Tk.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
u¿ywaj±cych tej biblioteki.

%package devel
Summary:	Tk binding for OCaml - development part
Summary(pl):	Wi±zafghjjtrfhuuiikkigde   aga   ogramistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
Library for interfacing Objective Caml with the scripting language
Tcl/Tk.

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl
Biblioteka pozwalaj±ca na ³±czenie programów napisanych w OCamlu i
Tcl/Tk.

Pakiet ten zawiera pliki niezbêdne do tworzenia programów u¿ywaj±cych
tej biblioteki.

%prep
%setup -q -n camltk%{ver}
%patch0 -p1

%build
cp %{_datadir}/automake/{config,install}* .
%{__autoconf}
sed -e 's/^CPPFLAGS/#&/' rpm.config > pld.config
%configure --with-config=./pld.config
%{__make} all opt

cd support
mkdir tmp
cd tmp
ar x ../libcamltk.a
%{__cc} -shared -o ../dllcamltk.so *.o
cd ..
rm -rf tmp
cd ..

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/camltk
%{__make} install INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/camltk

install */dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/camltk
(cd $RPM_BUILD_ROOT%{_libdir}/ocaml && ln -s camltk/dll*.so .)

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/camltk
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/camltk/META <<EOF
requires = ""
version = "%{version}"
directory = "+camltk"
archive(byte) = "camltk.cma"
archive(native) = "camltk.cmxa"
archive(byte,frx) = "libfrx.cma"
archive(native,frx) = "libfrx.cmxa"
archive(byte,jpf) = "libfrx.cma"
archive(native,jpf) = "libfrx.cmxa"
linkopts = ""
EOF

gzip -9nf $RPM_BUILD_ROOT%{_libdir}/ocaml/camltk/*.mli
mv -f $RPM_BUILD_ROOT%{_libdir}/ocaml/camltk/*.mli.gz .

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/camltk
%attr(755,root,root) %{_libdir}/ocaml/camltk/*.so
%{_libdir}/ocaml/*.so

%files devel
%defattr(644,root,root,755)
%doc LICENSE README
%{_libdir}/ocaml/camltk/*.cm[ixa]*
%{_libdir}/ocaml/camltk/*.a
%{_libdir}/ocaml/camltk/Makefile.camltk
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/camltk
