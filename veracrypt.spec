%ifarch %{ix86} %{arm} %{armx}
%define _disable_lto 1
%endif

# comment out when not a hotfix release
#define hotfix	Update2

Summary:	Disk encryption software
Name:		veracrypt
Version:	1.25.7
Release:	1
License:	Microsoft Public License
Group:		File tools
Url:		https://veracrypt.codeplex.com
Source0:	https://github.com/veracrypt/VeraCrypt/archive/VeraCrypt-VeraCrypt_%{version}%{?hotfix:-%hotfix}.tar.gz
BuildRequires:	wxgtku3.0-devel
BuildRequires:	makeself
BuildRequires:	nasm
BuildRequires:	pkgconfig(fuse)
BuildRequires:	imagemagick
BuildRequires:	yasm


%description
Free disk encryption software based on TrueCrypt.

%files
%doc %{_docdir}/%{name}/
%{_bindir}/%{name}
%{_sbindir}/mount.veracrypt
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/veracrypt.xml
%{_datadir}/veracrypt/languages/Language.*.xml
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/*

#----------------------------------------------------------------------------

%prep
%setup -qn VeraCrypt-VeraCrypt_%{version}%{?hotfix:-%hotfix}
%autopatch -p1

%build
export CC=gcc
export CXX=g++
pushd src
%make_build TC_EXTRA_LFLAGS+="%{ldflags} -ldl" \
            TC_EXTRA_CXXFLAGS="%{optflags}" \
            TC_EXTRA_CFLAGS="%{optflags}" \
            NOSTRIP=1 \
            VERBOSE=1
popd

pushd src/Resources/Icons
convert VeraCrypt-16x16.xpm VeraCrypt-16x16.png
convert VeraCrypt-48x48.xpm VeraCrypt-48x48.png
convert VeraCrypt-128x128.xpm VeraCrypt-128x128.png
popd

%install
pushd src
%make_install
popd

for png in 128x128 48x48 16x16; do
  mkdir -p %{buildroot}%{_iconsdir}/hicolor/${png}/apps/
  install -m 0644 src/Resources/Icons/VeraCrypt-${png}.png %{buildroot}%{_iconsdir}/hicolor/${png}/apps/%{name}.png
done

rm -rf %{buildroot}%{_bindir}/%{name}-uninstall.sh
