# ����Դ�ļ��к�Ŀ���ļ���·��
$source = "E:\������\8000-���ļ���\009-�����ļ���-��\005-209-Listary!2-����\�Զ�������"
$destination = "C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\"

# ���Դ�ļ����Ƿ����
if (-not (Test-Path -Path $source -PathType Container)) {
    Write-Error "Դ�ļ��в�����: $source"
    exit 1
}

# ���Ŀ���ļ����Ƿ���ڣ�����������򴴽�
if (-not (Test-Path -Path $destination -PathType Container)) {
    New-Item -ItemType Directory -Path $destination | Out-Null
    Write-Host "�Ѵ���Ŀ���ļ���: $destination"
}

try {
    # �ݹ鸴��Ŀ¼���ļ��������ļ��ṹ
    Copy-Item -Path "$source\*" -Destination $destination -Recurse -Force -ErrorAction Stop
    Write-Host "������ɣ�ԴĿ¼: $source �� Ŀ��Ŀ¼: $destination"
}
catch {
    Write-Error "���ƹ����з�������: $_"
    exit 2
}