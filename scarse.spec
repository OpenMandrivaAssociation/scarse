%define rversion 0.3-alpha
%define release  %mkrel 10
%define name scarse
%define version 0.3_alpha

Summary: Color calibration and management package
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Url: http://www.scarse.org/
Group: Graphics 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source: %{name}-%{rversion}.tar.bz2
BuildRequires: tiff-devel

%description
Scarse is a free color calibration and management software package. It
lets you build and use ICC profiles. Custom profiles can be generated
from a variety of calibration targets. Scarse is intended for (and
developed on) Unix machines and is distributed under the terms of the GNU
Public License (see file COPYING).

%prep
rm -rf $RPM_BUILD_ROOT

%setup -n %{name}-%{rversion}

%build
# patch makefiles to pass params ($(MAKE) instead of "make")
for i in Makefile src/Makefile icclib/Makefile; do
	perl -pi -e "s| make| \\$\(MAKE)||g;" $i
done

# patch prefix in {icclib,src,data}/Makefile
for i in data/Makefile src/Makefile icclib/Makefile; do
	perl -pi -e "s|/usr/local|%{_prefix}||g;" $i
done

# patch src/targets.c (patch from Sourceforge for 0.3_alpha)
perl -pi -e "s|stdin|0||g;" src/targets.c

# patch CFLAGS to include OTHER_CFLAGS in {icclib,src}/Makefile
for i in src/Makefile icclib/Makefile; do
	perl -pi -e "s|-m486 -O6 |\\$\(OTHER_CFLAGS) -fPIC ||g;" $i
done

# actual build
make OTHER_CFLAGS="$RPM_OPT_FLAGS" all

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
make PREFIX=$RPM_BUILD_ROOT%{_prefix} install

# move calibrate to scarse-calibrate to avoid ghostscript RPM conflict
( cd $RPM_BUILD_ROOT%{_bindir}; mv calibrate scarse-calibrate )

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES COPYING CREDITS INSTALL README TODO VERSION data/targets/TARGETS 
%{_bindir}/*
%{_libdir}/*
%dir %{_datadir}/cms/
%dir %{_datadir}/cms/etc/
%{_datadir}/cms/etc/*
%dir %{_datadir}/cms/targets/
%{_datadir}/cms/targets/TARGETS
%dir %{_datadir}/cms/targets/faust/
%{_datadir}/cms/targets/faust/*
%dir %{_datadir}/cms/targets/kodak/
%{_datadir}/cms/targets/kodak/*
%dir %{_datadir}/cms/targets/macbeth/
%{_datadir}/cms/targets/macbeth/*
%dir %{_datadir}/cms/targets/misc/
%{_datadir}/cms/targets/misc/*

